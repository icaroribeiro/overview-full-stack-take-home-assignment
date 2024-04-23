import { MakePredictionContext } from "../contexts/MakePredictionContext";
import { useContext, useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";
import { fabric } from "fabric";

function DrawPredictedImage() {
  const state = useContext<any>(MakePredictionContext);

  const [isRunning, setRunning] = useState(false);

  useEffect(() => {
    generatePredictedImage();
  }, [isRunning]);

  const generatePredictedImage = () => {
    if (isRunning) {
      try {
        const canvas = new fabric.Canvas("canvas");
        const image = URL.createObjectURL(state.imageData.file);
        fabric.Image.fromURL(image, function (img) {
          canvas.setHeight(img.height!);
          canvas.setWidth(img.width!);
          canvas.add(img);

          const detection_list = state.prediction.detection_list;
          for (let i = 0; i < detection_list.length; i++) {
            const height = detection_list[i].box.height;
            const left = detection_list[i].box.left;
            const top = detection_list[i].box.top;
            const width = detection_list[i].box.width;
            const rect = new fabric.Rect({
              height: height,
              left: left,
              top: top,
              width: width,
              fill: "yellow",
            });
            canvas.add(rect);
          }
          canvas.renderAll();
        });
      } catch (error) {
        console.error(`Failed to generate predicted image:`, error);
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
            <b>Create Predicted Image</b>
          </Form.Label>
          <br></br>
          <Button variant="primary" disabled={isRunning} onClick={handleClick}>
            {isRunning ? "Creating image…" : "Click here"}
          </Button>
          <br></br>
          <canvas id="canvas" />
        </Form.Group>
      </Form>
    </div>
  );
}

export default DrawPredictedImage;
