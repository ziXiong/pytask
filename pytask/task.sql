# 任务存储表
CREATE TABLE t_task (
  id       INT PRIMARY KEY AUTO_INCREMENT ,
  biz_num  VARCHAR(100) NOT NULL, # 业务关联代码
  biz_code VARCHAR(50)  NOT NULL, # 任务场景编码
  `when`     DATETIME     NOT NULL, # 执行时间点
  biz_ext TEXT, # 扩展信息
  create_time DATETIME NOT NULL, # 创建时间
  update_time DATETIME NOT NULL, # 修改时间
  status TINYINT NOT NULL DEFAULT 0, # 状态
  version INT NOT NULL DEFAULT 0 # 版本
);

#. 索引
CREATE UNIQUE INDEX idx_task_biz ON t_task(biz_num, biz_code);
CREATE INDEX idx_task_when ON t_task(`when`);
ALTER TABLE t_task
ADD CONSTRAINT num_code_unique UNIQUE  (biz_num, biz_code)