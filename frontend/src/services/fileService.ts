export const uploadFile = async (file: File): Promise<Response> => {
  const formData = new FormData();
  formData.append("video", file);

  const response = await fetch(
    `${import.meta.env.VITE_API_URL}video/upload_video`,
    {
      method: "POST",
      body: formData,
    }
  );

  return response;
};
