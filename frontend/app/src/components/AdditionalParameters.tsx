import { useContext } from "react";
import Form from "react-bootstrap/Form";
import { MakePredictionDispatchContext } from "../contexts/MakePredictionContext";
import { setConfidenceAction } from "../states/actions/setConfidenceAction";
import { setIouAction } from "../states/actions/setIouAction";

function AdditionalParameters() {
  const dispatch = useContext(MakePredictionDispatchContext);

  const handleConfidenceChange = (event) => {
    dispatch(setConfidenceAction(parseFloat(event.target.value)));
  };

  const handleIouChange = (event) => {
    dispatch(setIouAction(parseFloat(event.target.value)));
  };

  return (
    <Form>
      <Form.Group>
        <br></br>
        <Form.Label>
          <b>Configure Additional Prediction Parameters</b>
        </Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter the Confidence Value"
          onChange={handleConfidenceChange}
        />
        <br></br>
        <Form.Control
          type="text"
          placeholder="Enter the Iou Value"
          onChange={handleIouChange}
        />
      </Form.Group>
    </Form>
  );
}

export default AdditionalParameters;
