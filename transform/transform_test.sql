-- ----------------------------
-- 修改安卓和ios配置表的表名
-- ----------------------------
ALTER TABLE common_mobile_history RENAME TO mobile_history;
ALTER TABLE common_mobile_version RENAME TO mobile_version;
ALTER TABLE common_mobile_service RENAME TO mobile_service;
ALTER TABLE common_smscode RENAME TO mobile_smscode;

-- ----------------------------
-- 删除旧的日志表，并加入新的系统日志表
-- ----------------------------
DROP TABLE IF EXISTS `common_oper_log`;
DROP TABLE IF EXISTS `interact_bizlog`;
CREATE TABLE `interact_bizlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NULL DEFAULT NULL,
  `user_type` smallint(5) UNSIGNED NULL DEFAULT NULL,
  `user_school_id` smallint(5) UNSIGNED NULL DEFAULT NULL,
  `request` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `head` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `method` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `url` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `response` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `c` int(11) NULL DEFAULT NULL,
  `m` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `status_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ua` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `version` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ip` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `request_time` datetime(6) NULL DEFAULT NULL,
  `response_time` datetime(6) NULL DEFAULT NULL,
  `duration` int(11) NULL DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- 通用表的表格名称修改
-- ----------------------------
ALTER TABLE common_image RENAME TO interact_common_image;
ALTER TABLE common_file RENAME TO interact_common_file;
ALTER TABLE common_voice RENAME TO interact_common_voice;
ALTER TABLE common_video RENAME TO interact_common_video;

-- ----------------------------
-- 修改全局表表名，并清空内容（暂不使用）
-- ----------------------------
ALTER TABLE common_global RENAME TO interact_global;
DELETE FROM interact_global;

-- ----------------------------
-- 删除聊天相关表格
-- ----------------------------
DROP TABLE IF EXISTS `chat_class_para`;
DROP TABLE IF EXISTS `chat_group_invite`;
DROP TABLE IF EXISTS `chat_school_para`;
DROP TABLE IF EXISTS `chat_single_para`;

-- ----------------------------
-- 通信录群组表格表名修改
-- ----------------------------
ALTER TABLE chat_group RENAME TO interact_contacts_group;
ALTER TABLE chat_group_member RENAME TO interact_contacts_group_member;
ALTER TABLE interact_contacts_group DROP COLUMN chat_id;
ALTER TABLE interact_contacts_group DROP COLUMN chat_id_status;

-- ----------------------------
-- 删除授课表，内容已由用户中心接管
-- ----------------------------
DROP TABLE IF EXISTS `common_teachclass`;

-- ----------------------------
-- 修改圈子表的表名
-- ----------------------------
ALTER TABLE moment_base RENAME TO interact_moment;
ALTER TABLE moment_attach_file RENAME TO interact_moment_file;
ALTER TABLE moment_attach_image RENAME TO interact_moment_image;
ALTER TABLE moment_attach_video RENAME TO interact_moment_video;
ALTER TABLE moment_attach_voice RENAME TO interact_moment_voice;
ALTER TABLE moment_vote RENAME TO interact_moment_vote;
ALTER TABLE moment_vote_item RENAME TO interact_moment_vote_item;
ALTER TABLE moment_vote_user RENAME TO interact_moment_vote_user;
ALTER TABLE moment_like RENAME TO interact_moment_like;
ALTER TABLE moment_read RENAME TO interact_moment_read;
ALTER TABLE moment_reply RENAME TO interact_moment_reply;
ALTER TABLE moment_circle_class RENAME TO interact_moment_circle_class;
ALTER TABLE moment_circle_school RENAME TO interact_moment_circle_school;

-- ----------------------------
-- 增加请假互动、评价互动等3张表
-- ----------------------------
DROP TABLE IF EXISTS `interact_moment_dayoff`;
CREATE TABLE `interact_moment_dayoff`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `moment_id` int(11) NOT NULL,
  `is_visible_for_teacher` smallint(5) UNSIGNED NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_moment_d_moment_id_8f179899e83ef5_fk_interact_moment_id`(`moment_id`) USING BTREE,
  CONSTRAINT `interact_moment_d_moment_id_8f179899e83ef5_fk_interact_moment_id` FOREIGN KEY (`moment_id`) REFERENCES `interact_moment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `interact_moment_evaluate`;
CREATE TABLE `interact_moment_evaluate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `moment_id` int(11) NOT NULL,
  `type` smallint(5) UNSIGNED NOT NULL,
  `is_visible_for_parent_related` smallint(5) UNSIGNED NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_moment_moment_id_5ed2c2d31b6e85d5_fk_interact_moment_id`(`moment_id`) USING BTREE,
  CONSTRAINT `interact_moment_moment_id_5ed2c2d31b6e85d5_fk_interact_moment_id` FOREIGN KEY (`moment_id`) REFERENCES `interact_moment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `interact_moment_evaluate_student`;
CREATE TABLE `interact_moment_evaluate_student`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `moment_id` int(11) NOT NULL,
  `moment_evaluate_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_moment_moment_id_120a08ba6af8a057_fk_interact_moment_id`(`moment_id`) USING BTREE,
  INDEX `D09135a3fe6fb1e50751a2aa07ab7c06`(`moment_evaluate_id`) USING BTREE,
  INDEX `interact_moment_eva_student_id_2940d18d879a2a4b_fk_uc_student_id`(`student_id`) USING BTREE,
  CONSTRAINT `D09135a3fe6fb1e50751a2aa07ab7c06` FOREIGN KEY (`moment_evaluate_id`) REFERENCES `interact_moment_evaluate` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_moment_eva_student_id_2940d18d879a2a4b_fk_uc_student_id` FOREIGN KEY (`student_id`) REFERENCES `uc_student` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_moment_moment_id_120a08ba6af8a057_fk_interact_moment_id` FOREIGN KEY (`moment_id`) REFERENCES `interact_moment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- 通知表旧表全部删除、并新建新表
-- ----------------------------
DROP TABLE IF EXISTS `notify_attach_file`;
DROP TABLE IF EXISTS `notify_to_user`;
DROP TABLE IF EXISTS `notify_to_school`;
DROP TABLE IF EXISTS `notify_base`;

DROP TABLE IF EXISTS `interact_notify`;
CREATE TABLE `interact_notify`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `user_type` smallint(5) UNSIGNED NOT NULL,
  `user_school_id` int(11) NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `intro` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `type` smallint(5) UNSIGNED NOT NULL,
  `scope` smallint(5) UNSIGNED NOT NULL,
  `read_count` int(10) UNSIGNED NOT NULL,
  `has_voice` smallint(5) UNSIGNED NOT NULL,
  `has_image` smallint(5) UNSIGNED NOT NULL,
  `has_video` smallint(5) UNSIGNED NOT NULL,
  `has_file` smallint(5) UNSIGNED NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_notify_account_id_61b56f33dac1e1a3_fk_uc_account_id`(`account_id`) USING BTREE,
  INDEX `interact_notify_user_school_id_52de0376a55678_fk_uc_school_id`(`user_school_id`) USING BTREE,
  CONSTRAINT `interact_notify_account_id_61b56f33dac1e1a3_fk_uc_account_id` FOREIGN KEY (`account_id`) REFERENCES `uc_account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_notify_user_school_id_52de0376a55678_fk_uc_school_id` FOREIGN KEY (`user_school_id`) REFERENCES `uc_school` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `interact_notify_file`;
CREATE TABLE `interact_notify_file`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notify_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_notify__notify_id_9f1df925465b1dc_fk_interact_notify_id`(`notify_id`) USING BTREE,
  INDEX `interact_not_file_id_299c311f9db77a81_fk_interact_common_file_id`(`file_id`) USING BTREE,
  CONSTRAINT `interact_not_file_id_299c311f9db77a81_fk_interact_common_file_id` FOREIGN KEY (`file_id`) REFERENCES `interact_common_file` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_notify__notify_id_9f1df925465b1dc_fk_interact_notify_id` FOREIGN KEY (`notify_id`) REFERENCES `interact_notify` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `interact_notify_user_student`;
CREATE TABLE `interact_notify_user_student`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notify_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `is_read` smallint(5) UNSIGNED NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_notify_notify_id_6cce77e0acea74ab_fk_interact_notify_id`(`notify_id`) USING BTREE,
  INDEX `interact_notify_use_student_id_6eeaa7c9ebb4f554_fk_uc_student_id`(`student_id`) USING BTREE,
  CONSTRAINT `interact_notify_notify_id_6cce77e0acea74ab_fk_interact_notify_id` FOREIGN KEY (`notify_id`) REFERENCES `interact_notify` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_notify_use_student_id_6eeaa7c9ebb4f554_fk_uc_student_id` FOREIGN KEY (`student_id`) REFERENCES `uc_student` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- 修改interact_moment表的append_attr为textfield
-- 增加发动态人姓名字段
-- ----------------------------
ALTER TABLE interact_moment MODIFY COLUMN append_attr longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;
ALTER TABLE interact_moment ADD COLUMN user_name VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL;

-- ----------------------------
-- 修改interact_notify表的read_count为remind_count
-- ----------------------------
ALTER TABLE interact_notify change read_count remind_count smallint(5) UNSIGNED NOT NULL;

-- ----------------------------
-- 增加通知关联语音表
-- ----------------------------
DROP TABLE IF EXISTS `interact_notify_voice`;
CREATE TABLE `interact_notify_voice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notify_id` int(11) NOT NULL,
  `voice_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_del` smallint(5) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interact_notify_notify_id_4a5f9039f1dc3d3f_fk_interact_notify_id`(`notify_id`) USING BTREE,
  INDEX `interact_n_voice_id_119bc0d2358aaeb9_fk_interact_common_voice_id`(`voice_id`) USING BTREE,
  CONSTRAINT `interact_n_voice_id_119bc0d2358aaeb9_fk_interact_common_voice_id` FOREIGN KEY (`voice_id`) REFERENCES `interact_common_voice` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `interact_notify_notify_id_4a5f9039f1dc3d3f_fk_interact_notify_id` FOREIGN KEY (`notify_id`) REFERENCES `interact_notify` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- 生产环境版本落后，需要增加一个字段
-- ALTER TABLE mobile_version ADD COLUMN latest_version_checksum VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL;
-- ----------------------------
