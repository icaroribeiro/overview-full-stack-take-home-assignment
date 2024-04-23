export const setVideoDataAction = (id: string) => {
  return {
    type: "setVideoDataAction",
    payload: {
      id: id,
    },
  };
};
