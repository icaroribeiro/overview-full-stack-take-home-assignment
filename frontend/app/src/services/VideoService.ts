import UploadImageResponse from "../types/UploadImageResponse";
import VideoResponse from "../types/VideoResponse";
import api from "./api";

const registerVideo = async (name: string) => {
  try {
    const { data: response } = await api.post<VideoResponse>("/videos", {
      name: name,
    });
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const getVideosByName = async (name: string) => {
  try {
    const { data: response } = await api.get<[VideoResponse]>(
      `/videos?name=${name}`,
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const uploadImage = async (videoId: string, file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const { data: response } = await api.post<UploadImageResponse>(
      `/videos/${videoId}/upload-image`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );
    return response;
  } catch (error) {
    console.log("Caught error: ", error);
    throw error;
  }
};

const VideoService = {
  registerVideo,
  getVideosByName,
  uploadImage,
};

export default VideoService;
