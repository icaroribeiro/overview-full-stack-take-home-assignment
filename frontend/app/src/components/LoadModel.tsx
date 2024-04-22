import { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import PredictionService from "../services/PredictionService";
import FloatingLabel from "react-bootstrap/FloatingLabel";

function LoadModel() {
  const [modelName, setModelName] = useState("yolov8n");
  const [isRunning, setRunning] = useState(false);

  const handleModelNameChange = (event) => {
    setModelName(event.target.value);
  };

  useEffect(() => {
    loadModel();
  }, [isRunning]);

  const loadModel = async () => {
    if (isRunning) {
      try {
        const response = await PredictionService.loadModel(modelName);
        console.log(response);
      } catch (error) {
        console.error(`Failed to load model with name=${modelName}:`, error);
      } finally {
        console.warn("Api call done!");
        setRunning(false);
      }
    }
  };

  const handleClick = () => {
    if (isRunning) {
      return;
    }
    setRunning(true);
  };

  return (
    <div>
      <Form>
        <Form.Group>
          <br></br>
          <Form.Label>
            <b>Load the Prediction Model</b>
          </Form.Label>
          <FloatingLabel
            controlId="floatingSelect"
            label="Choose the Model Name"
          >
            <Form.Select
              aria-label="Floating label select example"
              onChange={handleModelNameChange}
            >
              <option value="yolov8n">yolov8n</option>
              <option value="yolov8s">yolov8s</option>
            </Form.Select>
          </FloatingLabel>
          <Button variant="primary" disabled={isRunning} onClick={handleClick}>
            {isRunning ? "Loading model…" : "Click here"}
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default LoadModel;
