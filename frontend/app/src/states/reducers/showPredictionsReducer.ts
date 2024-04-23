export default function (state: any, action: any) {
  switch (action.type) {
    case "setVideoDataAction":
      return { ...state, videoData: { id: action.payload.id } };
    case "setPredictionsAction":
      return { ...state, predictions: action.predictions };
    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}
