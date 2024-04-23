import PredictionResponse from "../../types/PredictionResponse";

export const setPredictionAction = (prediction: PredictionResponse) => {
  return {
    type: "setPredictionAction",
    prediction: prediction,
  };
};
