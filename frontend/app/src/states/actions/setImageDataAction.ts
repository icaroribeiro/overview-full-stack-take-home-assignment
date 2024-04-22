export const setImageDataAction = (file, path) => {
  return {
    type: "setImageDataAction",
    payload: {
      file: file,
      path: path,
    },
  };
};
