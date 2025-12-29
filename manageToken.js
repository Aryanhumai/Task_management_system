// var token = "";
// export const getToken = () => {
//   return token;
// };
// export const setToken = (newToken) => {
//   token = newToken;
// };

export const getToken = () => {
  return localStorage.getItem("token");
};

export const setToken = (newToken) => {
  localStorage.setItem("token", newToken);
};

export const clearToken = () => {
  localStorage.removeItem("token");
};
