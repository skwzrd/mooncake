<template>
  <div>
    <button class="information_toggle btn" @click="toggle">Information</button>
    <div class="info" v-if="this.information_toggle">
      <img src="mooncake_chinese.png"/>
      <div>
        🔹[Previous][Next] navigates through characters without submitting statistics to the server.
        <br>
        🔹[❌][✔️] will submit -/+ 1 statistic delta for a character.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Information',
  data() {
    return {
      information_toggle: false
    };
  },
  methods: {
    toggle() {
      this.information_toggle = !this.information_toggle;
    },
  }
}
</script>


<style scoped>
img {
  width: 200px;
  margin: 10px;
  border-color: #c5c8c6;
  border-width: 2px;
  border-radius: 2px;
  border-style: solid;
}

button {
  margin: 5px;
}

.info {
  background-color: #070808;
  border-color: #c5c8c6;
  border-width: 2px;
  border-radius: 2px;
  border-style: solid;
  padding: 5px;
}
</style>
