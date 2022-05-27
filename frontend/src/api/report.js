import { apiInstance } from "./index.js";

const api = apiInstance();

async function getRank(success, fail) {
  await api.get(`reports/rank/`).then(success).catch(fail);
}

async function getTimeReportList(success, fail) {
  await api.get(`reports/timereport/year/`).then(success).catch(fail);
}

export { getRank, getTimeReportList };
