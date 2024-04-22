import BBOXResponse from "./BBOXResponse";

export default interface DetectionResponse {
  box: BBOXResponse;
  class_name: string;
  confidence: number;
}
