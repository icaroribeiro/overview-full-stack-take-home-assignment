import { useContext, useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { ShowPredictionsDispatchContext } from "../contexts/ShowPredictionsContext";
import VideoService from "../services/VideoService";
import { setVideoDataAction } from "../states/actions/setVideoDataAction";

function SearchVideo() {
  const dispatch = useContext(ShowPredictionsDispatchContext);

  const [isRunning, setRunning] = useState(false);
  const [videoName, setVideoName] = useState("");

  const handleVideoNameChange = (event) => {
    setVideoName(event.target.value);
  };

  useEffect(() => {
    searchVideo();
  }, [isRunning]);

  const searchVideo = async () => {
    if (isRunning) {
      try {
        const response = await VideoService.getVideosByName(videoName);
        console.log(response);
        dispatch(setVideoDataAction(response[0].id));
      } catch (error) {
        console.error(`Failed to search video with name=${videoName}:`, error);
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
          <Form.Label>
            <b>Search the Video</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter the Video Name"
            value={videoName}
            onChange={handleVideoNameChange}
          />
          <Button variant="primary" disabled={isRunning} onClick={handleClick}>
            {isRunning ? "Searching video…" : "Click here"}
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default SearchVideo;
