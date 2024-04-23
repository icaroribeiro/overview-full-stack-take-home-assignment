import { ChangeEvent, useContext, useEffect, useState } from "react";
import {
  MakePredictionContext,
  MakePredictionDispatchContext,
} from "../contexts/MakePredictionContext";
import { Button, Form } from "react-bootstrap";
import VideoService from "../services/VideoService";
import Image from "react-bootstrap/Image";
import { setImageDataAction } from "../states/actions/setImageDataAction";

function UploadImage() {
  const state = useContext<any>(MakePredictionContext);
  const dispatch = useContext<any>(MakePredictionDispatchContext);

  const [isRunning, setRunning] = useState(false);
  const [file, setFile] = useState(new File([""], "filename"));

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      setFile(files[0]);
    }
  };

  useEffect(() => {
    uploadImage();
  }, [isRunning]);

  const uploadImage = async () => {
    if (isRunning) {
      const videoId = state.videoData.id;

      try {
        const response = await VideoService.uploadImage(videoId, file);
        dispatch(setImageDataAction(file, response.path));
      } catch (error) {
        console.error(
          `Failed to upload image with video id=${videoId}:`,
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
          <br></br>
          <Form.Label>
            <b>Upload the Image</b>
          </Form.Label>
          <br></br>
          <Form.Label>Choose the Image</Form.Label>
          <Form.Control type="file" onChange={handleFileChange} />
          <Image src={URL.createObjectURL(file)} />
          <br></br>
          <Button variant="primary" disabled={isRunning} onClick={handleClick}>
            {isRunning ? "Uploading image…" : "Click here"}
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default UploadImage;
