<template>
  <div>
    <div id="titleBox">
      <h1 id="title">Cyber Maxlevel Coach 🧘🏻</h1>
      <p>운동을 하면서 AI 자세 분석 서비스를 받을 수 있는 곳입니다.</p>
    </div>
    <div id="infoBox">
      <div class="boxGroup">
        <img src="@/assets/info1.png" alt="info1" class="box">
        <div class="box">
          <p class="manual">
            유튜브에서 오늘 진행할 홈트 영상을 찾으세요.<br> 영상을 클릭하고 위의 주소창에서 주소를 입력하세요.<br>
            사진과 같은 구도로 운동을 하시면 AI가 동작을 분석해서<br> 차이점을 음성으로 지적해줍니다.<br>
            운동이 끝나면 운동 분석 레포트로 얼마나 운동했는지 알 수 있습니다!
          </p>
        </div>
      </div>
    </div>

    <div id="infoBox">
      <div class="boxGroup">
        <div class="box">
          <p class="manual2">
            마이페이지에선 스케줄링 기능을 제공합니다.<br>
            운동한 날 달력에 표시를 해줍니다.<br> 초록색으로 성실하게 운동했는지 알 수 있어요.<br>
            원하는 운동날짜와 시간을 선택하면<br> 카카오톡을 통해 알림을 드립니다.<br>
            빼먹지 말고 운동하세요!<br>
            그냥 운동만하면 심심하죠! 운동기록을 통해 다른유저와 경쟁!<br> 운동을 열심히한 순으로 랭킹을 매겨드립니다!<br>
          </p>
        </div>
        <img src="@/assets/info2.png" alt="info1" class="box">
      </div>
    </div>
  </div>
  <br />
</template>

<script>

export default {
  name: "ProgramIntro",
  data() {
    return {

    }
  },
  methods: {

  }
};
</script>

<style>

#title {
  font-family: 'Anton', sans-serif;
  font-weight: bold;
  /* color: black; */
  margin-bottom: 30px;
}

#titleBox {
  margin-bottom: 70px;
  padding-top: 50px;
}

#infoBox {
  margin-bottom: 30px;
}

.boxGroup {
  display: flex;
  flex-wrap: wrap;
  /* justify-content: space-evenly; */
}

.box {
  /* height: 400px; */
  /* border: 2px solid black; */
  flex: 1 1 40%;
  margin: 0px 40px;
}

.manual {
  margin-top: 50px;
  margin-bottom: 50px;
  text-align: left;
  font-weight: bold;
  font-size: 1.5rem;
  vertical-align: middle;
  line-height: 1.7;
}

.manual2 {
  margin-top: 50px;
  margin-bottom: 50px;
  margin-right: 20px;
  text-align: right;
  font-weight: bold;
  font-size: 1.5rem;
  vertical-align: middle;
  line-height: 1.7;
}

</style>
