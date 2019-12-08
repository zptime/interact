export class AbsFileMgr {
  constructor(name) {
    this.name = name;
  }

  fun1() {
    alert("hello world");
  }

  set desc(value) {
    this.desc = value;
  }

  get desc() {
    return this.desc;
  }
}
