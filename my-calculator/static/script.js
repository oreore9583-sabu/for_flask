
function addinput(new_input) {
const Value=document.getElementById("siki").value;
if(new_input=="clear"){
document.getElementById("siki").value="";}
else if(new_input=="delete"){
document.getElementById("siki").value=Value.slice(0,-1);
}
else{document.getElementById("siki").value=Value+new_input;}


}
function make_button(){
  for(let i=1;i<10;i++){
    // 1. button要素を作成
    const btn = document.createElement("button");

    // 2. ボタンのテキスト（ラベル）を設定
    btn.textContent = i;
    btn.id = i;
    if(i!=3&&i!=6&&i!=9){btn.style="margin-right:4px;";
                        }
    
    // 3. クリックイベントを追加
    btn.addEventListener("click",function(){addinput(this.id);} );
    if(0<i&&i<4){
    
    const container = document.getElementById("0-3");
    container.appendChild(btn);
    }
    else if(3<i&&i<7){
      const container = document.getElementById("4-6");
      container.appendChild(btn);
    } 
    else if(6<i&&i<10){
      const container = document.getElementById("7-9");
      container.appendChild(btn);
      
    }
  }
}
make_button();
