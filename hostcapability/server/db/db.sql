CREATE  TABLE `nova`.`host_capability` (
  `id` INT NOT NULL ,
  `host` VARCHAR(45) NULL ,
  `ip` VARCHAR(45) NULL ,
  `rack` VARCHAR(45) NULL ,
  `vtd_enabled_eth` TINYINT(1)  NULL ,
  `has_node_manager` TINYINT(1)  NULL ,
  `updated_at` DATETIME NULL ,
  `deleted_at` DATETIME NULL ,
  `deleted` TINYINT(1)  NULL ,
  PRIMARY KEY (`id`) );