export default function (state, action) {
  switch (action.type) {
    case "setVideoDataAction":
      return { ...state, videoData: { id: action.payload.id } };
    case "setImageDataAction":
      return {
        ...state,
        imageData: { file: action.payload.file, path: action.payload.path },
      };
    case "setConfidenceAction":
      return { ...state, confidence: action.confidence };
    case "setIouAction":
      return { ...state, iou: action.iou };
    case "setPredictionAction":
      return { ...state, prediction: action.prediction };
    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}
