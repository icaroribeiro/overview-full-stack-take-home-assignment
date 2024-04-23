import { ChangeEvent, useContext, useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { MakePredictionDispatchContext } from "../contexts/MakePredictionContext";
import VideoService from "../services/VideoService";
import { setVideoDataAction } from "../states/actions/setVideoDataAction";

function RegisterVideo() {
  const dispatch = useContext<any>(MakePredictionDispatchContext);

  const [isRunning, setRunning] = useState(false);
  const [videoName, setVideoName] = useState("");

  const handleVideoNameChange = (event: ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value
    if (value) {
      setVideoName(value)
    }
  };

  useEffect(() => {
    registerVideo();
  }, [isRunning]);

  const registerVideo = async () => {
    if (isRunning) {
      try {
        const response = await VideoService.registerVideo(videoName);
        dispatch(setVideoDataAction(response.id));
      } catch (error) {
        console.error(
          `Failed to register video with name=${videoName}:`,
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
    <div>
      <Form>
        <Form.Group>
          <Form.Label>
            <b>Register the Video</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter the Video Name"
            value={videoName}
            onChange={handleVideoNameChange}
          />
          <Button variant="primary" disabled={isRunning} onClick={handleClick}>
            {isRunning ? "Registering video…" : "Click here"}
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default RegisterVideo;
