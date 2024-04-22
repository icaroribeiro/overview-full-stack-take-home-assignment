import { useReducer } from "react";
import LoadModel from "../components/LoadModel";
import {
  MakePredictionContext,
  MakePredictionDispatchContext,
} from "../contexts/MakePredictionContext";
import makePredictionReducer from "../states/reducers/makePredictionReducer";
import RegisterVideo from "../components/RegisterVideo";
import AdditionalPredictionParams from "../components/AdditionalParameters";
import PrintPredictionRecord from "../components/PrintPredictionRecord";
import UploadImage from "../components/UploadImage";
import DrawPredictedImage from "../components/DrawPredictedImage";

const initialState = {};

function MakePrediction() {
  const [state, dispatch] = useReducer(makePredictionReducer, initialState);

  return (
    <MakePredictionContext.Provider value={state}>
      <MakePredictionDispatchContext.Provider value={dispatch}>
        <RegisterVideo />
        <UploadImage />
        <LoadModel />
        <AdditionalPredictionParams />
        <PrintPredictionRecord />
        <DrawPredictedImage />
      </MakePredictionDispatchContext.Provider>
    </MakePredictionContext.Provider>
  );
}

export default MakePrediction;
