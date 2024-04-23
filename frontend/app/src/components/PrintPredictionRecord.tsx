import { useContext, useEffect, useState } from "react";
import Table from "react-bootstrap/Table";
import PredictionResponse from "../types/PredictionResponse";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import PredictionService from "../services/PredictionService";
import {
  MakePredictionContext,
  MakePredictionDispatchContext,
} from "../contexts/MakePredictionContext";
import { setPredictionAction } from "../states/actions/setPredictionAction";

function PrintPredictionRecord() {
  const state = useContext<any>(MakePredictionContext);
  const dispatch = useContext<any>(MakePredictionDispatchContext);

  const [isRunning, setRunning] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse>();

  useEffect(() => {
    createPrediction();
  }, [isRunning]);

  const createPrediction = async () => {
    if (isRunning) {
      const videoId = state.videoData.id;
      const imagePath = state.imageData.path;
      const confidence = state.confidence;
      const iou = state.iou;

      try {
        const response = await PredictionService.createPrediction(
          videoId,
          imagePath,
          confidence,
          iou,
        );
        setPrediction(response);
        dispatch(setPredictionAction(response));
      } catch (error) {
        console.error(
          `Failed to create prediction with videoId=${videoId}, imagePath=${imagePath}, confidence=${confidence} and iou=${iou}:`,
          error,
        );
      } finally {
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
    <Form>
      <Form.Group>
        <br></br>
        <Form.Label>
          <b>Create the Image Prediction Record</b>
        </Form.Label>
        <br></br>
        <Button variant="primary" disabled={isRunning} onClick={handleClick}>
          {isRunning ? "Creating record…" : "Click here"}
        </Button>
        <br></br>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>id</th>
              <th>video_id</th>
              <th>image_path</th>
              <th>model_name</th>
              <th>confidence</th>
              <th>iou</th>
              <th>detection_list</th>
              <th>created_at</th>
            </tr>
          </thead>
          <tbody>
            {prediction && (
              <tr key={0}>
                <td>{prediction.id}</td>
                <td>{prediction.video_id}</td>
                <td>{prediction.image_path}</td>
                <td>{prediction.model_name}</td>
                <td>{prediction.confidence}</td>
                <td>{prediction.iou}</td>
                <td>
                  {prediction.detection_list
                    .map(
                      (item) => `{
                "box": {
                  "height": ${item.box.height},
                  "left": ${item.box.left},
                  "top": ${item.box.top},
                  "width": ${item.box.width},
              },
              "class_name": ${item.class_name},
              "confidence": ${item.confidence}
            }`,
                    )
                    .join(",")}
                </td>
                <td>{prediction.created_at.toString()}</td>
              </tr>
            )}
          </tbody>
        </Table>
        <br></br>
      </Form.Group>
    </Form>
  );
}

export default PrintPredictionRecord;
