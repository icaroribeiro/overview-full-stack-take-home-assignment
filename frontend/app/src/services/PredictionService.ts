import IGetLoadedModelResponse from "../types/LoadedModelResponse";
import ILoadedModel from "../types/LoadModelResponse";
import PredictionResponse from "../types/PredictionResponse";
import api from "./api";

const loadModel = async (name: string) => {
  try {
    const { data: response } = await api.post<ILoadedModel>(
      "/predictions/load-model",
      {
        name: name,
      },
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const getLoadedModel = async () => {
  try {
    const { data: response } = await api.get<IGetLoadedModelResponse>(
      "/predictions/get-loaded-model",
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const createPrediction = async (
  videoId: string,
  imagePath: string,
  confidence: number,
  iou: number,
) => {
  try {
    const { data: response } = await api.post<PredictionResponse>(
      "/predictions",
      {
        video_id: videoId,
        image_path: imagePath,
        confidence: confidence,
        iou: iou,
      },
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const getPredictions = async (
  videoId: string,
  sortType: string = "desc",
  limit: number,
) => {
  try {
    const { data: response } = await api.get<PredictionResponse[]>(
      `/predictions?video_id=${videoId}&sort_type=${sortType}&limit=${limit}`,
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const PredictionService = {
  loadModel,
  getLoadedModel,
  createPrediction,
  getPredictions,
};

export default PredictionService;
