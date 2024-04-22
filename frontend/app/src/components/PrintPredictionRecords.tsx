import { useContext, useEffect, useState } from "react";
import { ShowPredictionsContext } from "../contexts/ShowPredictionsContext";
import Table from "react-bootstrap/Table";
import PredictionResponse from "../types/PredictionResponse";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import PredictionService from "../services/PredictionService";

function PrintPredictionRecords() {
  const state = useContext(ShowPredictionsContext);

  const [isRunning, setRunning] = useState(false);
  const [predictions, setPredictions] = useState<PredictionResponse[]>([]);

  useEffect(() => {
    getPredictions();
  }, [isRunning]);

  const getPredictions = async () => {
    if (isRunning) {
      const videoId = state.videoData.id;
      const sortType = "desc";
      const limit = 10;

      try {
        const response = await PredictionService.getPredictions(
          videoId,
          sortType,
          limit,
        );
        console.log(response);
        setPredictions(response);
      } catch (error) {
        console.error(
          `Failed to get predictions with videoId=${videoId}, sortType=${sortType} and limit=${limit}:`,
          error,
        );
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
    <Form>
      <Form.Group>
        <br></br>
        <Form.Label>
          <b>Get The 10 Most Recent Video Prediction Records</b>
        </Form.Label>
        <br></br>
        <Button variant="primary" disabled={isRunning} onClick={handleClick}>
          {isRunning ? "Getting records…" : "Click here"}
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
            {predictions &&
              predictions.map((item, index) => (
                <tr key={index}>
                  <td>{item.id}</td>
                  <td>{item.video_id}</td>
                  <td>{item.image_path}</td>
                  <td>{item.model_name}</td>
                  <td>{item.confidence}</td>
                  <td>{item.iou}</td>
                  <td>
                    {item.detection_list
                      .map(
                        (item) => `{
                "box": {
                  "height": ${item.box.height},
                  "left": ${item.box.left},
                  "top":  ${item.box.top},
                  "width":  ${item.box.width},
              },
              "class_name": ${item.class_name},
              "confidence": ${item.confidence}
            }`,
                      )
                      .join(",")}
                  </td>
                  <td>{item.created_at.toString()}</td>
                </tr>
              ))}
          </tbody>
        </Table>
      </Form.Group>
    </Form>
  );
}

export default PrintPredictionRecords;
