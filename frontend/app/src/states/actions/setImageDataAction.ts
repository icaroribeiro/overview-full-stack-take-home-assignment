export const setImageDataAction = (file: File, path: string) => {
  return {
    type: "setImageDataAction",
    payload: {
      file: file,
      path: path,
    },
  };
};
