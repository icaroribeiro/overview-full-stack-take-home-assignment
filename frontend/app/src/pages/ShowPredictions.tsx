import SearchVideo from "../components/SearchVideo";
import showPredictionsReducer from "../states/reducers/showPredictionsReducer";
import { useReducer } from "react";
import {
  ShowPredictionsContext,
  ShowPredictionsDispatchContext,
} from "../contexts/ShowPredictionsContext";
import PrintPredictionRecords from "../components/PrintPredictionRecords";

const initialState = {};

function ShowPredictions() {
  const [state, dispatch] = useReducer(showPredictionsReducer, initialState);

  return (
    <ShowPredictionsContext.Provider value={state}>
      <ShowPredictionsDispatchContext.Provider value={dispatch}>
        <SearchVideo />
        <PrintPredictionRecords />
      </ShowPredictionsDispatchContext.Provider>
    </ShowPredictionsContext.Provider>
  );
}

export default ShowPredictions;
