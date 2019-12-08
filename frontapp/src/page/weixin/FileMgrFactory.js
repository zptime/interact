import {AbsFileMgr} from "./AbsFileMgr";
import {HXNativeFileMgr} from "./HXNativeFileMgr";

export function createFileMgr(type) {
  if (type == '1') {
    return new AbsFileMgr("abs file mgr");
  } else {
    return new HXNativeFileMgr("HX Native File Mgr");
  }
}
