import axios from "axios";
import { API_BASE_URL } from "@/config";

function getCookie(cookie_name) {
  // 출처 : https://webisfree.com/2015-02-04/[%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8]-%EC%BF%A0%ED%82%A4(cookie)-%EC%A0%80%EC%9E%A5-%EB%B0%8F-%EC%82%AD%EC%A0%9C-%EC%98%88%EC%A0%9C%EB%B3%B4%EA%B8%B0
  var x, y;
  var val = document.cookie.split(";");

  for (var i = 0; i < val.length; i++) {
    x = val[i].substr(0, val[i].indexOf("="));
    y = val[i].substr(val[i].indexOf("=") + 1);
    x = x.replace(/^\s+|\s+$/g, ""); // 앞과 뒤의 공백 제거하기
    if (x == cookie_name) {
      return unescape(y); // unescape로 디코딩 후 값 리턴
    }
  }
  return undefined;
}

function apiInstance() {
  const authorization = getCookie("cmc_token");
  if (!authorization) {
    // TODO : 로그인이 해제되었습니다 ~~>
  }

  const instance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      "Content-type": "application/json",
      Authorization: `${localStorage.getItem("jwt")}`,
    },
  });
  return instance;
}

export { apiInstance, getCookie };
