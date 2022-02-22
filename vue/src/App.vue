<template>
  <div>
    <div id="information">
      <Information/>
    </div>
    <div id="dashboard" class="main" v-if="this.study_session_in_progress">
      <CharacterCard ref="CharacterCard"/>
    </div>
    <div v-else class="main configs">
      <div>
        <div>HSK: 
          <select v-model="hsk_level" class="btn">
            <option v-for="n in hsk_levels" :key="n" :value="n" class="btn">{{n}}</option>
          </select>
        </div>
        <div>Size:
          <select v-model="size" class="btn">
            <option v-for="n in getNumbers(size_min, size_max, 2)" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
        <div>Study Type: 
          <select v-model="study_type" class="btn">
            <option v-for="n in study_types" :key="n" :value="n" class="btn">{{n}}</option>
          </select>
        </div>
      </div>
      <br>
      <div>
        <button @click="toggle_study_session_in_progress" class="btn">Start</button>
      </div>
    </div>
  </div>
</template>

<script>
import CharacterCard from './components/CharacterCard.vue'
import Information from './components/Information.vue'

export default {
  name: 'App',
  components: {
    Information,
    CharacterCard,
  },
  data(){
    return {
      study_session_in_progress: false,
      hsk_levels: 6,
      hsk_level: 1,
      study_types: ['New', 'Known', 'Equally Mixed'],
      study_type: 'Equally Mixed',
      size: 10,
      size_max: 20,
      size_min: 2,
    }
  },
  methods: {
    toggle_study_session_in_progress() {
      this.study_session_in_progress = !this.study_session_in_progress;
    },
    getNumbers(start, stop, step=2){
      return new Array(stop / step).fill(start).map((n, i)=>(i+1)*step);
    },
  }
}
</script>

<style>
body{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #1d1f21;
  color: #c5c8c6;
}

#information {
  max-width: 500px;
}

.main {
  text-align: center;
  margin-top: 40px;
  position: relative;
  margin: auto;
}

.configs {
  font-size: 30px;
}

.btn {
  font: inherit;
  background-color: transparent;
  cursor: pointer;
  color: rgb(125, 139, 167);
  padding: 5px;
  border: 1px solid rgb(125, 139, 167);
  border-radius: 2px;
}

.btn:active {
  color: #2d3d4d;
  text-decoration: none;
  cursor: pointer;
}

button + button {
  margin-left: 15px;
}

button {
  width: 6em;
  margin-bottom: 15px;
}
</style>
