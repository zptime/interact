//返回角度
export const GetSlideAngle = (dx,dy) => {
  return Math.atan2(dy,dx) * 180 / Math.PI;
};

//根据起点和终点返回方向 1：向上，2：向下，3：向左，4：向右,0：未滑动
//返回角度
export const GetSlideDirection = (startX,startY, endX, endY) => {
  let dy = startY - endY;
  let dx = endX - startX;
  let result = 0;
  //如果滑动距离太短
  if (Math.abs(dx) < 2 && Math.abs(dy) < 2) {
    return result;
  }

  let angle = GetSlideAngle(dx, dy);
  if (angle >= -45 && angle < 45) {
    result = 4;
  }else if (angle >= 45 && angle < 135) {
    result = 1;
  }else if (angle >= -135 && angle < -45) {
    result = 2;
  }else if ((angle >= 135 && angle <= 180) || (angle >= -180 && angle < -135)) {
    result = 3;
  }
  return result;
};

export const Touch = (scroll,touchEle) => {
  let myBody = document.getElementsByTagName('body')[0];

  //滑动处理
  let startX, startY;
  myBody.addEventListener('touchstart', function (ev){
    startX = ev.touches[0].pageX;
    startY = ev.touches[0].pageY;
  }, {passive: true});

  let endX, endY;
  myBody.addEventListener('touchmove', function (ev){
    endX = ev.changedTouches[0].pageX;
    endY = ev.changedTouches[0].pageY;

    let direction = GetSlideDirection(startX, startY, endX, endY);
    let myPublish = document.getElementsByClassName(touchEle)[0];
    switch (direction){
      case 0:
        break;
        return 0;
      case 1:
        if(scroll && myPublish){
          myPublish.style.display='none';
        }
        break;
        return 1;
      case 2:
        if(scroll && myPublish){
          myPublish.style.display='block';
        }
        break;
        return 2;
      case 3:
        break;
        return 3;
      case 4:
        break;
        return 4;
      default:
        return '';
    }
  }, {passive: true});
};

