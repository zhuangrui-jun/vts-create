<script setup lang="ts">
import { ref } from 'vue'

const DISMISS_KEY = 'introduction_dismissed'
const visible = ref(!localStorage.getItem(DISMISS_KEY))

function open() {
  visible.value = true
}
function close() {
  visible.value = false
  localStorage.setItem(DISMISS_KEY, '1')
}

defineExpose({ open })
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="intro-overlay" @click.self="close">
      <div class="intro-modal">
        <button class="intro-close" @click="close" title="关闭">✕</button>
        <div class="intro-content">
          <p>八百代们，各位神明，今天过的还好吗？</p>
          <br />

          <p>《超时空辉夜姬》牛福！<br />
          感觉辉夜姬二刷很好看呀，不过三刷也好看，<br />
          但是四刷更好看，比起四刷其实五刷更好看，<br />
          虽然五刷好看 但有一说一六刷更好看，听说七刷比六刷更好看，<br />
          个人认为八刷比七刷好看，即便如此八刷还是没九刷好看，<br />
          等等十刷似乎是更好看，十一刷十二刷应该是比十刷好看……</p>
          <br />

          <p>作者看完《超时空辉夜姬》之后，感觉已是世界上最空虚的人了<br />
          在此空虚之际，看到了deepseek v4的横空出世，于是心血来潮<br />
          用ds v4+claude code进行了一波harness engineering<br />
          该说不说，作者虽然没怎么深入过py，但利用ai还是完整地做了出来<br />
          不得不感慨ai的强大，有了harness连报错都很少出现了，最主要的还是业务地考究和提示词地完善以及plan<br />
          开发时间约一周，时间比较琐碎，要比较好多次方案的选择，边学习边成长</p>
          <br />

          <p>主要的功能是live2d加载以及大模型的对话功能，尽量还原八千代的人物形象<br />
          （其实挺想做tts语音合成的，但是训练出来的太抽象了，就不搞了）</p>
          <hr />

          <h2>具体功能介绍：</h2>

          <ul>
            <li><strong>live2d表情智能化</strong><br />能通过语境反映人物心情，并映射到live2d身上</li>
            <li><strong>表情包发送</strong><br />每轮对话都会发送一个对应的表情包（表情包检索这一块比较繁琐，做的不是很好，表情包的种类太多了，容易跟语境很不符合），为了节省资源，表情包没有放在上下文中，也不会放在数据库中（怕污染上下文），所以刷新之后之前的表情包都会消失。</li>
            <li><strong>大模型对话</strong>
              <ul>
                <li>框架：langgraph</li>
                <li>记忆功能</li>
                <li>联网搜索tool</li>
              </ul>
            </li>
          </ul>
          <hr />

          <p>最后总结一下，个人觉得逻辑业务方面不是很好，有改进的地方，后续有时间会进行优化（感觉记忆、联网方面只是用来回顾以前做的大模型对话的知识吧，现在大模型api是可以直接提供这些功能的）</p>
          <br />

          <p><strong>（此项目纯个人爱好驱使，未经作者准许不得用于商业等用途）</strong></p>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.intro-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  animation: fadeIn .2s ease;
}
.intro-modal {
  position: relative;
  width: min(640px, 90vw);
  max-height: 85vh;
  background: #1e1e2e;
  border: 1px solid #555;
  border-radius: 12px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, .5);
  overflow: hidden;
  animation: slideUp .25s ease;
}
.intro-close {
  position: absolute;
  top: 10px;
  right: 14px;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color .15s, background .15s;
  z-index: 1;
}
.intro-close:hover {
  color: #fff;
  background: rgba(255, 255, 255, .1);
}
.intro-content {
  padding: 28px 32px 32px;
  overflow-y: auto;
  max-height: calc(85vh - 60px);
  color: #e8e6e3;
  font-size: 14px;
  line-height: 1.75;
}
.intro-content :deep(h1) { font-size: 22px; color: #fff; margin: 0 0 12px; }
.intro-content :deep(h2) {
  font-size: 17px; color: #f2f0ee; margin: 24px 0 10px;
  padding-bottom: 6px; border-bottom: 1px solid #555;
}
.intro-content :deep(h3) { font-size: 15px; color: #edeae6; margin: 16px 0 6px; }
.intro-content :deep(hr) { border: none; border-top: 1px solid #555; margin: 20px 0; }
.intro-content :deep(ul) { margin: 6px 0; padding-left: 20px; }
.intro-content :deep(li) { margin: 4px 0; }
.intro-content :deep(table) { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px; }
.intro-content :deep(th) {
  text-align: left; padding: 6px 12px; background: rgba(255,255,255,.08);
  color: #edeae6; font-weight: 600; border: 1px solid #555;
}
.intro-content :deep(td) { padding: 5px 12px; border: 1px solid #555; color: #e8e6e3; }
.intro-content :deep(blockquote) {
  margin: 10px 0; padding: 8px 16px; border-left: 3px solid #999;
  background: rgba(255,255,255,.05); color: #d5d2ce;
}
.intro-content :deep(strong) { color: #f2f0ee; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
