import {AbsFileMgr} from "./AbsFileMgr";

export class HXNativeFileMgr extends AbsFileMgr{
  constructor(name) {
    super(name);
    this.name = name;
  }

  fun1() {
    alert("hello new world");
  }
}
