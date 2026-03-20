// MODIFICATION NOTICE:
// This file was created programmatically to fix the Hand Swapping bug
// in the Hybrid Holistic architecture.
// Compatible with MediaPipe v0.10.21.

// Copyright 2026 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <cmath>
#include <vector>
#include <memory>
#include <limits>

#include "absl/memory/memory.h"
#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/formats/detection.pb.h"
#include "mediapipe/framework/formats/location_data.pb.h"
#include "mediapipe/framework/port/status.h"

namespace mediapipe {

// A Calculator that takes a vector of Detections and outputs a vector
// containing only the single Detection whose bounding box center is closest
// to the center of the image (0.5, 0.5 in normalized coordinates).
// This is critical for preventing "Hand Swapping" in recrop-based pipelines
// when using a general object detector (like PalmDetection SSD) instead of
// a regression network.
//
// Input:
//  DETECTIONS: std::vector<Detection>
//
// Output:
//  DETECTIONS: std::vector<Detection> containing max 1 element.
class ClosestToCenterDetectionCalculator : public CalculatorBase {
 public:
  static absl::Status GetContract(CalculatorContract* cc) {
    RET_CHECK(cc->Inputs().HasTag("DETECTIONS"));
    RET_CHECK(cc->Outputs().HasTag("DETECTIONS"));

    cc->Inputs().Tag("DETECTIONS").Set<std::vector<Detection>>();
    cc->Outputs().Tag("DETECTIONS").Set<std::vector<Detection>>();

    return absl::OkStatus();
  }

  absl::Status Open(CalculatorContext* cc) override {
    cc->SetOffset(TimestampDiff(0));
    return absl::OkStatus();
  }

  absl::Status Process(CalculatorContext* cc) override {
    if (cc->Inputs().Tag("DETECTIONS").IsEmpty()) {
      return absl::OkStatus();
    }

    const auto& detections =
        cc->Inputs().Tag("DETECTIONS").Get<std::vector<Detection>>();
    
    auto output_detections = absl::make_unique<std::vector<Detection>>();

    if (detections.empty()) {
      cc->Outputs().Tag("DETECTIONS").Add(output_detections.release(), cc->InputTimestamp());
      return absl::OkStatus();
    }

    int closest_index = -1;
    float min_distance_sq = std::numeric_limits<float>::max();

    for (int i = 0; i < detections.size(); ++i) {
      const Detection& detection = detections[i];
      if (!detection.location_data().has_relative_bounding_box()) {
        continue;
      }
      const auto& bbox = detection.location_data().relative_bounding_box();
      if (std::isnan(bbox.xmin()) || std::isnan(bbox.ymin()) || 
          std::isnan(bbox.width()) || std::isnan(bbox.height())) {
        continue;
      }
      
      // Calculate center of the bounding box
      float x_center = bbox.xmin() + bbox.width() / 2.0f;
      float y_center = bbox.ymin() + bbox.height() / 2.0f;

      // Distance to (0.5, 0.5)
      float dx = x_center - 0.5f;
      float dy = y_center - 0.5f;
      float distance_sq = dx * dx + dy * dy;

      if (distance_sq < min_distance_sq) {
        min_distance_sq = distance_sq;
        closest_index = i;
      }
    }

    if (closest_index != -1) {
      output_detections->push_back(detections[closest_index]);
    }

    cc->Outputs().Tag("DETECTIONS").Add(output_detections.release(), cc->InputTimestamp());
    return absl::OkStatus();
  }
};

REGISTER_CALCULATOR(ClosestToCenterDetectionCalculator);

}  // namespace mediapipe
