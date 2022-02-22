<template>
  <div>
    <div>
      <div class="chinese" @click="play_character_audio">{{ current_character.chinese }}</div>
      <div v-if="show_pinyin">{{ current_character.pinyin }}</div><div v-else>.</div>
      <div v-if="show_definition">{{ current_character.english }}</div><div v-else>.</div>
    </div>
    <br>
    <div id="controls">
      <div>
        <button @click="get_previous_character" class="btn">Previous<br>🇶</button>
        <button @click="get_next_character" class="btn">Next<br>🇼</button>
      </div>
      <div>
        <button @click="play_character_audio" class="btn">Audio<br>🇦</button>
        <button @click="toggle_pinyin" class="btn">Pinyin<br>🇸</button>
        <button @click="toggle_show_definition" class="btn">Definition<br>🇩</button>
      </div>
      <div>
        <button @click="set_stat_one_minus" class="btn">❌<br>⬅️</button>
        <button @click="set_stat_one_plus" class="btn">✔️<br>➡️</button>
      </div>
      <div>
        <a href="/"><button class="btn">Abort Session</button></a>
      </div>
      <div>
        {{ this.current_index + 1 }} / {{ this.character_count }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';


function get_data(url, callback){
  axios.get(url)
  .then((response) => {
    callback(response.data)
  })
  .catch((response, status, error) => {
    alert(`${url}, ${response}, ${status}, ${error}`);
  })
}

function post_data(url, data){
  axios.post(url, data)
  .then((response) => {
    return response;
  })
  .catch((response, status, error) => {
    alert(`${url}, ${response}, ${data}, ${status}, ${error}`);
  })
}

export default {
  name: 'CharacterCard',
  data() {
    return {
      characters: {},
      character_count: 0,
      current_character: {},
      current_index: null,
      character_audio: {},
      show_definition: false,
      show_pinyin: false,
      queue: [],
    }
  },
  mounted() {
    let self = this; 
    window.addEventListener('keyup', function(e) {
        self.keyUpControl(e);
    });
  },
  created() {
    this.init();
  },
  methods: {
    init(){
      get_data(`${this.get_server_url()}/study_session?type=${this.$parent.study_type.toLowerCase().replace(' ', '_')}&size=${this.$parent.size}&hsk=${this.$parent.hsk_level}`,
        characters => {
          this.characters = characters;
          this.character_count = Object.keys(this.characters).length;
          this.queue = this.generate_queue();
          this.get_next_character();
        }
      );
    },
    get_server_url(){
      let network_ip = window.location.host.split(':')[0];
      return `http://${network_ip}:5000`; // flask on local port 5000;
    },
    keyUpControl(e){
      const key = e.key.toLowerCase();

      if(key == 'a'){
        this.play_character_audio();
      }
      else if(key == 's'){
        this.toggle_pinyin();
      }
      else if(key == 'd'){
        this.toggle_show_definition();
      }

      else if(key == 'q'){
        this.get_previous_character();
      }
      else if(key == 'w'){
        this.get_next_character();
      }

      else if(key == 'arrowleft'){
        this.set_stat_one_minus();
      }
      else if(key == 'arrowright'){
        this.set_stat_one_plus();
      }

    },
    play_character_audio(){
      this.get_character_audio();
      this.character_audio[this.current_index].play();
    },
    stop_character_audio(){
      this.character_audio[this.current_index].pause();
    },
    get_character_audio(){
      if (!this.character_audio[this.current_index]){
        this.character_audio[this.current_index] = new Audio(`${this.get_server_url()}/audio/` + this.current_character.chinese)
      }
    },
    generate_queue(){
      return Array.from(Array(this.character_count).keys());
    },
    get_next_character(){
      if (this.queue.length === 0){
        alert('Done!')
        this.$parent.toggle_study_session_in_progress();
      }
      if (this.character_audio[this.current_index]){
        this.stop_character_audio();
      }

      if (this.current_index + 1 < this.queue[0]){
        this.current_index += 1;
      }
      else{
        this.current_index = this.queue.shift();
      }
      this.current_character = this.characters[this.current_index];

      this.show_definition = false;
    },
    toggle_show_definition(){
      this.show_definition = !this.show_definition;
    },
    toggle_pinyin(){
      this.show_pinyin = !this.show_pinyin;
    },
    get_previous_character(){
      if (this.character_audio[this.current_index]){
        this.stop_character_audio();
      }
      if (this.current_index > 0){
        this.current_index -= 1;
        this.current_character = this.characters[this.current_index];
        this.show_definition = false;
      }
    },
    set_stat_one_minus(){
      post_data(`${this.get_server_url()}/character_stat`, {user_id: 1, character_id: this.current_character.index, delta: -1})
      this.get_next_character();
    },
    set_stat_one_plus(){
      post_data(`${this.get_server_url()}/character_stat`, {user_id: 1, character_id: this.current_character.index, delta: 1})
      this.get_next_character();
    },
  },
}
</script>


<style>
.chinese {
  font-size: 6em;
  display: inline-block;
}

.chinese:hover {
  cursor: pointer;
  color: #7e7e7e;
}

#controls {
  position: relative;
  margin-top: 20em;
  margin: auto;
  display: inline-block;
}

</style>
