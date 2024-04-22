import DetectionResponse from "./DetectionResponse";

export default interface PredictionResponse {
  id: string;
  video_id: string;
  model_name: string;
  image_path: string;
  confidence: number;
  iou: number;
  detection_list: DetectionResponse[];
  created_at: Date;
}
