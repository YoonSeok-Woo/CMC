<template>
  <div id="outer" style="height: 69vh;">
    <b-container fluid>
    <b-row class="mt-5 mb-2">
      <b-col cols="6">
        <input type="text" v-model="youtube_link" class="mx-2" style="height: 38px; width: 450px" />
        <button @click="youtube_src">
          유튜브 주소 입력
        </button>
      </b-col>
      <b-col cols="6">
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="6">
        <div id="video_wrapper">
          <YoutubeVue3
            ref="youtube"
            :videoid="play.video_id"
            :loop="0"
            :width="720"
            :height="480"
            @ended="onEnded"
            @paused="onPaused"
            @played="onPlayed"
            :autoplay="0"
            :controls="1"
          />
        </div>
      </b-col>
      <b-col cols="6">
        <div>
          <video
            id="webcam"
            width="720"
            height="480"
            autoplay
            muted
            playsinline
          ></video>
        </div>
      </b-col>
    </b-row>
    </b-container>
    <!-- <div id="screen_wrapper">
      <video
        id="screen"
        width="960"
        height="540"
        autoplay
        muted
        playsinline
      ></video>
    </div> -->
  </div>
  <div id="player"></div>
</template>

<script>
import axios from "axios";
import { API_BASE_URL } from "@/config";
import { YoutubeVue3 } from "youtube-vue3";
import * as poseDetection from "@tensorflow-models/pose-detection";
import "@tensorflow/tfjs-backend-webgl";

export default {
  name: "Excercise",
  components: { YoutubeVue3 },
  data() {
    return {
      play: { video_id: "", loop: 1 },
      youtube_link: "",
      speaking: "",
      player: null,
      video_id: "",
      loop: true,
      start_time: null,
      end_time: null,
      check_start: false,
      check_promise: false,
      posetime: -1,
      interval: "",
      good_sentence: [
        "잘 따라하고 있어요",
        "좋아요",
        "최고에요",
        "멋져요",
        "아주 잘 하고 있어요",
      ],
    };
  },
  methods: {
    tts: function (str) {
      const sentence = `<speak>${str}</speak>`;
      const headers = {
        "Content-Type": "application/xml",
        Authorization: "KakaoAK 9b0514e3984268ec50947549b669d0d6",
      };
      axios({
        method: "post",
        url: "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",
        headers: headers,
        data: sentence,
        responseType: "arraybuffer",
      }).then(function (res) {
        const context = new AudioContext();
        context.decodeAudioData(res.data, (buffer) => {
          const source = context.createBufferSource();
          source.buffer = buffer;
          source.connect(context.destination);
          source.start(0);
        });
      });
    },
    record_time: function () {
      console.log("!!!!!!!!!");
      axios({
        method: "post",
        url: API_BASE_URL + "reports/timereport/",
        headers: { Authorization: localStorage.getItem("jwt") },
        data: {
          timereport_time: parseInt((this.end_time - this.start_time) / 60000),
        },
      })
        .then((res) => {
          console.log(res);
          this.endWebcam();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    calculateAngle(keypoints) {
      //5 왼쪽어깨 6 오른쪽어깨 7 왼쪽팔꿈치 8 오른쪽팔꿈치 9 왼쪽손목 10 오른쪽손목 11 왼쪽골반 12 오른쪽골반  13 왼쪽무릎 14 오른쪽무릎 15 왼쪽발목 16 오른쪽발목
      let anglearray = [];
      let arr2 = [
        [9, 7, 5, "왼쪽팔꿈치"],
        [10, 8, 6, "오른쪽팔꿈치"],
        [7, 5, 11, "왼쪽겨드랑이"],
        [8, 6, 12, "오른쪽겨드랑이"],
        [13, 11, 12, "왼쪽아래골반"],
        [14, 12, 11, "오른쪽아래골반"],
        [11, 13, 15, "왼쪽무릎"],
        [12, 14, 16, "오른쪽무릎"],
      ];
      for (var i = 0; i < arr2.length; i++) {
        var arr = arr2[i];
        var angle1 = Math.atan2(
          keypoints[arr[1]].y - keypoints[arr[0]].y,
          keypoints[arr[0]].x - keypoints[arr[1]].x
        );
        var angle2 = Math.atan2(
          keypoints[arr[1]].y - keypoints[arr[2]].y,
          keypoints[arr[2]].x - keypoints[arr[1]].x
        );
        var angle3 = Math.abs(((angle1 - angle2) * 180) / Math.PI);
        if (angle3 > 180) {
          angle3 = 360 - angle3;
        }
        angle3 = Math.round(angle3);
        anglearray.push([arr[3], angle3]);
      }
      return anglearray;
    },
    youtube_src: function () {
      var source = this.youtube_link;
      var code = source.split("v=")[1].split("&t=")[0];
      const temp = { video_id: code, loop: 1 };
      this.play = Object.assign(this.play, temp);
      //this.$refs.youtube.player.stopVideo()
    },
    async posenet() {
      const videoElement = document.querySelector("iframe");
      const target = videoElement;
      const offsetY = document
        .querySelector("#nav_group")
        .getBoundingClientRect().height;
      const track = videoElement.srcObject.getVideoTracks()[0].clone();
      const imageCapture = new ImageCapture(track);
      const image = await imageCapture.grabFrame();
      const youtubecanvas = document.createElement("canvas");
      const content = youtubecanvas.getContext("2d");
      youtubecanvas.width = target.width;
      youtubecanvas.height = target.height;
      const x = target.getBoundingClientRect().x;
      const y = target.getBoundingClientRect().y + offsetY;
      const width = target.getBoundingClientRect().width;
      const height = target.getBoundingClientRect().height;
      content.drawImage(image, x, y, width, height, 0, 0, width, height);
      image.close();
      track.stop();
      const model = poseDetection.SupportedModels.MoveNet;
      const detectorConfig = {
        modelType: poseDetection.movenet.modelType.SINGLEPOSE_THUNDER,
        enableTracking: true,
        trackerType: poseDetection.TrackerType.BoundingBox,
      };
      const webcam = document.getElementById("webcam");
      poseDetection.createDetector(model, detectorConfig).then((net) => {
        Promise.all([
          net.estimatePoses(youtubecanvas),
          net.estimatePoses(webcam),
        ]).then((pose) => {
          console.log("well done")
          const webcamarray = this.calculateAngle(pose[1][0].keypoints);
          const youtubearray = this.calculateAngle(pose[0][0].keypoints);
          const resultarray = [];
          for (var i = 0; i < webcamarray.length; i++) {
            resultarray.push([
              webcamarray[i][0],
              webcamarray[i][1] - youtubearray[i][1],
            ]);
          }
          resultarray.sort(function (a, b) {
            if (a[1] < b[1]) {
              return -1;
            }
            if (a[1] > b[1]) {
              return 1;
            }
            return 0;
          });
          if (!this.check_promise) {
            if (Math.abs(resultarray[0][1]) > Math.abs(resultarray[7][1])) {
              //음수일 때 = 각도가 더 작다
              const angle = Math.abs(resultarray[0][1]);
              if (angle > 20 && angle < 40) {
                var str = resultarray[0][0] + "을 조금만 더 벌려주세요";
                this.tts(str);
              } else if (angle > 40 && angle < 60) {
                str = resultarray[0][0] + "을 많이 벌려주세요";
                this.tts(str);
              } else if (angle <= 20) {
                this.tts(this.good_sentence[this.randomNum(0, 4)]);
              } else {
                if(this.posetime==-1){
                  this.posetime= new Date()

                  this.tts("자세나 카메라를 조정해주세요")
                  
                }else{
                  const now = new Date()
                  if((now-this.posetime)>=15000){
                    this.posetime= new Date()
                    this.tts("자세나 카메라를 조정해주세요")
                  }
                }
              }
            } else {
              const angle = Math.abs(resultarray[7][1]);
              if (angle > 20 && angle < 40) {
                str = resultarray[7][0] + "을 조금만 더 오므려주세요";
                this.tts(str);
              } else if (angle > 40 && angle < 60) {
                str = resultarray[0][0] + "을 많이 오므려주세요";
                this.tts(str);
              } else if (angle <= 20) {
                this.tts(this.good_sentence[this.randomNum(0, 4)]);
              } else {
                if(this.posetime==-1){
                  this.posetime= new Date()

                  this.tts("자세나 카메라를 조정해주세요")
                  
                }else{
                  const now = new Date()
                  if((now-this.posetime)>=15000){
                    this.posetime= new Date()
                    this.tts("자세나 카메라를 조정해주세요")
                  }
                }
              }
            }
          }
        }).catch((err) => {
          console.log(err)
          console.log("well done")
        });
      });
    },
    onPlayed() {
      clearInterval(this.interval);
      this.start_time = new Date();
      if (!this.check_start) {
        this.playShare();
        this.check_start = true;
      }
      this.playWebcam();
      this.interval = setInterval(this.posenet, 5000);
    },
    onEnded() {
      this.end_time = new Date();
      clearInterval(this.interval);
      this.record_time();
    },
    onPaused() {
      this.end_time = new Date();
      clearInterval(this.interval);
      this.record_time();
    },
    playWebcam() {
      const webcam = document.getElementById("webcam");
      navigator.mediaDevices
        .getUserMedia({ video: { width: 960, height: 540 }, audio: false })
        .then(function (stream) {
          webcam.srcObject = stream;
        })
        .catch(function (e) {
          console.log(e);
        });
    },
    async playShare() {
      const videoElement = document.querySelector("iframe");
      try {
        const displayMediaOptions = {
          audio: false,
          video: { cursor: "always" },
        };
        const captureStream = await navigator.mediaDevices.getDisplayMedia(
          displayMediaOptions
        );
        videoElement.srcObject = captureStream;
      } catch (err) {
        console.error(err);
      }
    },
    endWebcam() {
      const video = document.getElementById("webcam");
      const tracks1 = video.srcObject.getTracks();
      tracks1.forEach((track) => track.stop());
      video.srcObject.null;
    },
    randomNum(min, max) {
      var randNum = Math.floor(Math.random() * (max - min + 1)) + min;
      return randNum;
    },
  },
};
</script>

<style scoped></style>
