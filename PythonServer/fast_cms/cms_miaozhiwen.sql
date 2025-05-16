/*
 Navicat Premium Dump SQL

 Source Server         : 本地MySQL
 Source Server Type    : MySQL
 Source Server Version : 80025 (8.0.25)
 Source Host           : localhost:3306
 Source Schema         : cms_miaozhiwen

 Target Server Type    : MySQL
 Target Server Version : 80025 (8.0.25)
 File Encoding         : 65001

 Date: 16/05/2025 21:50:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_category_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2061 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '商品分类表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES (2, '上衣', '2021-04-19 00:00:00', '2021-04-19 00:00:00');
INSERT INTO `categories` VALUES (3, '裤子', '2021-04-19 07:56:27', '2021-04-19 07:56:27');
INSERT INTO `categories` VALUES (4, '鞋子', '2021-04-19 07:56:31', '2021-04-19 07:56:31');
INSERT INTO `categories` VALUES (5, '厨具', '2021-04-20 00:00:00', '2021-04-20 00:00:00');
INSERT INTO `categories` VALUES (6, '家具', '2021-04-20 00:00:00', '2021-04-20 00:00:00');
INSERT INTO `categories` VALUES (7, '床上用品', '2021-04-20 01:00:00', '2021-04-20 01:00:00');
INSERT INTO `categories` VALUES (8, '女装', '2021-04-21 00:00:00', '2021-04-21 00:00:00');
INSERT INTO `categories` VALUES (2060, '床上用品dsasda', '2025-05-15 15:47:58', '2025-05-15 15:47:58');

-- ----------------------------
-- Table structure for departments
-- ----------------------------
DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '部门ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '部门名称',
  `parentId` int NULL DEFAULT NULL COMMENT '父部门ID (逻辑外键, 指向 departments.id)',
  `leader` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门领导',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '部门表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of departments
-- ----------------------------
INSERT INTO `departments` VALUES (1, '总裁办', NULL, 'coderwhy', '2021-01-02 10:03:09', '2021-01-05 08:25:46');
INSERT INTO `departments` VALUES (2, '人事部das', 1, 'coderwhy', '2025-05-15 15:46:20', '2025-05-15 15:46:20');
INSERT INTO `departments` VALUES (4, '客服部', 2, 'lily', '2021-01-02 10:04:02', '2021-08-03 11:14:32');

-- ----------------------------
-- Table structure for menus
-- ----------------------------
DROP TABLE IF EXISTS `menus`;
CREATE TABLE `menus`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '类型:1一级菜单,2二级菜单,3按钮权限',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单URL',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `sort` int NULL DEFAULT NULL COMMENT '排序',
  `permission` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识字符串 (按钮权限)',
  `parentId` int NULL DEFAULT NULL COMMENT '父菜单ID (逻辑外键, 指向 menus.id)',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_menu_permission`(`permission` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menus
-- ----------------------------
INSERT INTO `menus` VALUES (1, '系统管理', 1, '/main/system', 'el-icon-setting', 2, NULL, NULL, '2021-01-02 10:08:14', '2021-08-20 07:00:08');
INSERT INTO `menus` VALUES (2, '用户管理', 2, '/main/system/user', NULL, 100, NULL, 1, '2021-01-02 18:08:47', '2021-08-19 15:52:01');
INSERT INTO `menus` VALUES (3, '部门管理', 2, '/main/system/department', NULL, 101, NULL, 1, '2021-01-02 18:09:11', '2021-08-19 15:52:04');
INSERT INTO `menus` VALUES (4, '菜单管理', 2, '/main/system/menu', NULL, 103, NULL, 1, '2021-01-02 18:09:22', '2021-08-19 15:52:07');
INSERT INTO `menus` VALUES (5, '创建用户', 3, NULL, NULL, NULL, 'system:users:create', 2, '2021-01-03 13:41:01', '2021-08-19 16:10:06');
INSERT INTO `menus` VALUES (6, '删除用户', 3, NULL, NULL, NULL, 'system:users:delete', 2, '2021-01-03 13:41:01', '2021-08-19 16:10:21');
INSERT INTO `menus` VALUES (7, '修改用户', 3, NULL, NULL, NULL, 'system:users:update', 2, '2021-01-03 13:41:01', '2021-08-19 16:10:24');
INSERT INTO `menus` VALUES (8, '查询用户', 3, NULL, NULL, NULL, 'system:users:query', 2, '2021-01-03 13:41:01', '2021-08-19 16:10:26');
INSERT INTO `menus` VALUES (9, '商品中心', 1, '/main/product', 'el-icon-goods', 3, NULL, NULL, '2021-01-05 12:15:56', '2021-08-20 07:00:25');
INSERT INTO `menus` VALUES (10, '删除故事', 3, NULL, NULL, NULL, 'system:story:delete', 43, '2021-01-03 13:41:01', '2021-04-19 21:59:44');
INSERT INTO `menus` VALUES (11, '修改故事', 3, NULL, NULL, NULL, 'system:story:update', 43, '2021-01-03 13:41:01', '2021-04-19 21:59:47');
INSERT INTO `menus` VALUES (12, '查询故事', 3, NULL, NULL, NULL, 'system:story:query', 43, '2021-01-03 13:41:01', '2021-04-19 21:59:49');
INSERT INTO `menus` VALUES (15, '商品类别', 2, '/main/product/category', NULL, 104, NULL, 9, '2021-04-19 21:55:11', '2021-08-19 15:52:12');
INSERT INTO `menus` VALUES (16, '商品信息', 2, '/main/product/goods', NULL, 105, NULL, 9, '2021-04-19 21:57:33', '2021-08-19 15:52:14');
INSERT INTO `menus` VALUES (17, '创建部门', 3, NULL, NULL, NULL, 'system:department:create', 3, '2021-01-03 13:41:01', '2021-04-19 21:59:39');
INSERT INTO `menus` VALUES (18, '删除部门', 3, NULL, NULL, NULL, 'system:department:delete', 3, '2021-01-03 13:41:01', '2021-04-19 22:05:07');
INSERT INTO `menus` VALUES (19, '修改部门', 3, NULL, NULL, NULL, 'system:department:update', 3, '2021-01-03 13:41:01', '2021-04-19 22:05:11');
INSERT INTO `menus` VALUES (20, '查询部门', 3, NULL, NULL, NULL, 'system:department:query', 3, '2021-01-03 13:41:01', '2021-04-19 22:05:14');
INSERT INTO `menus` VALUES (21, '创建菜单', 3, NULL, NULL, NULL, 'system:menu:create', 4, '2021-01-03 13:41:01', '2021-04-19 21:59:39');
INSERT INTO `menus` VALUES (22, '删除菜单', 3, NULL, NULL, NULL, 'system:menu:delete', 4, '2021-01-03 13:41:01', '2021-04-19 22:05:18');
INSERT INTO `menus` VALUES (23, '修改菜单', 3, NULL, NULL, NULL, 'system:menu:update', 4, '2021-01-03 13:41:01', '2021-04-19 22:05:21');
INSERT INTO `menus` VALUES (24, '查询菜单', 3, NULL, NULL, NULL, 'system:menu:query', 4, '2021-01-03 13:41:01', '2021-04-19 22:05:24');
INSERT INTO `menus` VALUES (25, '角色管理', 2, '/main/system/role', NULL, 102, NULL, 1, '2021-01-02 18:09:22', '2021-08-19 15:52:17');
INSERT INTO `menus` VALUES (26, '创建角色', 3, NULL, NULL, NULL, 'system:role:create', 25, '2021-01-03 13:41:01', '2021-04-19 21:59:39');
INSERT INTO `menus` VALUES (27, '删除角色', 3, NULL, NULL, NULL, 'system:role:delete', 25, '2021-01-03 13:41:01', '2021-04-19 21:59:44');
INSERT INTO `menus` VALUES (28, '修改角色', 3, NULL, NULL, NULL, 'system:role:update', 25, '2021-01-03 13:41:01', '2021-04-19 21:59:47');
INSERT INTO `menus` VALUES (29, '查询角色', 3, NULL, NULL, NULL, 'system:role:query', 25, '2021-01-03 13:41:01', '2021-04-19 21:59:49');
INSERT INTO `menus` VALUES (30, '创建类别', 3, NULL, NULL, NULL, 'system:category:create', 15, '2021-01-03 13:41:01', '2021-04-19 21:59:39');
INSERT INTO `menus` VALUES (31, '删除类别', 3, NULL, NULL, NULL, 'system:category:delete', 15, '2021-01-03 13:41:01', '2021-04-19 21:59:44');
INSERT INTO `menus` VALUES (32, '修改类别', 3, NULL, NULL, NULL, 'system:category:update', 15, '2021-01-03 13:41:01', '2021-04-19 21:59:47');
INSERT INTO `menus` VALUES (33, '查询类别', 3, NULL, NULL, NULL, 'system:category:query', 15, '2021-01-03 13:41:01', '2021-04-19 21:59:49');
INSERT INTO `menus` VALUES (34, '创建商品', 3, NULL, NULL, NULL, 'system:goods:create', 16, '2021-01-03 13:41:01', '2021-08-19 17:29:46');
INSERT INTO `menus` VALUES (35, '删除商品', 3, NULL, NULL, NULL, 'system:goods:delete', 16, '2021-01-03 13:41:01', '2021-08-19 17:29:50');
INSERT INTO `menus` VALUES (36, '修改商品', 3, NULL, NULL, NULL, 'system:goods:update', 16, '2021-01-03 13:41:01', '2021-08-19 17:29:53');
INSERT INTO `menus` VALUES (37, '查询商品', 3, NULL, NULL, NULL, 'system:goods:query', 16, '2021-01-03 13:41:01', '2021-08-19 17:30:02');
INSERT INTO `menus` VALUES (38, '系统总览', 1, '/main/analysis', 'el-icon-monitor', 1, NULL, NULL, '2021-04-19 14:11:02', '2021-08-20 06:59:55');
INSERT INTO `menus` VALUES (39, '核心技术', 2, '/main/analysis/overview', NULL, 106, NULL, 38, '2021-01-02 18:09:11', '2021-08-19 15:54:41');
INSERT INTO `menus` VALUES (40, '商品统计', 2, '/main/analysis/dashboard', NULL, 107, NULL, 38, '2021-01-02 18:09:22', '2021-08-19 15:56:08');
INSERT INTO `menus` VALUES (41, '随便聊聊', 1, '/main/story', 'el-icon-chat-line-round', 4, NULL, NULL, '2021-04-19 14:11:02', '2021-08-20 07:00:44');
INSERT INTO `menus` VALUES (42, '你的故事', 2, '/main/story/chat', NULL, 108, NULL, 41, '2021-01-02 18:09:11', '2021-08-19 17:29:31');
INSERT INTO `menus` VALUES (43, '故事列表', 2, '/main/story/list', NULL, 109, NULL, 41, '2021-01-02 18:09:11', '2021-08-19 15:52:29');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '商品名称',
  `oldPrice` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '原价 (接口返回字符串,存储为VARCHAR或DECIMAL)',
  `newPrice` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '现价 (接口返回字符串,存储为VARCHAR或DECIMAL)',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '商品描述',
  `status` int NULL DEFAULT 1 COMMENT '商品状态 (接口返回数字)',
  `imgUrl` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品图片URL',
  `inventoryCount` int NULL DEFAULT 0 COMMENT '库存数量',
  `saleCount` int NULL DEFAULT 0 COMMENT '销量',
  `favorCount` int NULL DEFAULT 0 COMMENT '收藏数量',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '发货地址/产地',
  `categoryId` int NULL DEFAULT NULL COMMENT '商品分类ID (逻辑外键, 指向 categories.id)',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 184 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '商品表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (173, '时尚套装韩版气质甜美镂空灯笼袖针织衫百搭显瘦毛衣女2018秋季新款连衣裙套装', '70', '70', '时尚套装韩版气质甜美镂空灯笼袖针织衫百搭显瘦毛衣女2018秋季新款连衣裙套装', 1, 'http://s11.mogucdn.com/mlcdn/c45406/180822_5bl46cl4g934133a6cbhkk8l37hl0_640x960.jpg_560x999.jpg', 1615, 1360, 286, '沈阳', 3, '2021-04-30 13:42:54', '2021-04-30 13:42:54');
INSERT INTO `products` VALUES (174, '2018秋季新款时尚套装蝴蝶结波点衬衫圆领麻花毛衣无袖马甲百褶半身裙中长款A字裙套装三件套', '86', '60', '2018秋季新款时尚套装蝴蝶结波点衬衫圆领麻花毛衣无袖马甲百褶半身裙中长款A字裙套装三件套', 1, 'http://s11.mogucdn.com/mlcdn/c45406/180131_1kgh02j1j4lbb74g0427ljk976612_640x960.jpg_560x999.jpg', 4118, 1356, 311, '青岛', 8, '2021-04-30 13:42:55', '2021-04-30 13:42:55');
INSERT INTO `products` VALUES (183, '吊带背心女夏2018秋季新款内搭吊带衫短款性感修身针织打底衫上衣显瘦', '43', '30', '吊带背心女夏2018秋季新款内搭吊带衫短款性感修身针织打底衫上衣显瘦', 1, 'http://s11.mogucdn.com/mlcdn/17f85e/180927_5i77e04lhaalbg3dai0j4588lbahh_640x960.jpg_560x999.jpg', 6285, 2, 3, '天津', 6, '2021-04-30 13:43:16', '2021-04-30 13:43:16');

-- ----------------------------
-- Table structure for role_menu
-- ----------------------------
DROP TABLE IF EXISTS `role_menu`;
CREATE TABLE `role_menu`  (
  `role_id` int NOT NULL COMMENT '角色ID (逻辑外键, 指向 roles.id)',
  `menu_id` int NOT NULL COMMENT '菜单ID (逻辑外键, 指向 menus.id)',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '分配时间',
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色菜单关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_menu
-- ----------------------------
INSERT INTO `role_menu` VALUES (1, 1, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 2, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 3, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 4, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 5, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 6, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 7, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 8, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 9, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 15, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 16, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 17, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 18, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 19, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 20, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 21, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 22, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 23, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 24, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 25, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 26, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 27, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 28, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 29, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 30, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 31, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 32, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 33, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 34, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 35, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 36, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 37, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 38, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 39, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 40, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 41, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 42, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (1, 43, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 1, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 2, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 3, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 4, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 5, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 6, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 7, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 8, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 9, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 15, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 16, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 17, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 18, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 19, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 20, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 21, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 22, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 23, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 24, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 25, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (4, 30, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 1, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 2, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 3, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 4, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 5, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 6, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 7, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 8, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 9, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 15, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 16, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 17, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 18, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 19, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 20, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 21, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 22, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 23, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 24, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 25, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 26, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 27, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 28, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 29, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 30, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 31, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 32, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 33, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 34, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 35, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 36, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 37, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 38, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 39, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 40, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 41, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 42, '2025-05-16 15:15:35');
INSERT INTO `role_menu` VALUES (15228, 43, '2025-05-16 15:15:35');

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `intro` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色介绍',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_role_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15229 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES (1, '超级管理员', '所有权限', '2021-01-02 10:01:52', '2021-01-02 10:01:52');
INSERT INTO `roles` VALUES (3, '运营', '日常事务', '2021-01-05 11:47:42', '2021-01-05 11:50:11');
INSERT INTO `roles` VALUES (4, '人事', '人事管理', '2021-01-05 11:47:42', '2021-01-05 11:50:11');
INSERT INTO `roles` VALUES (15228, '运营2dasda', '日常管理2dassd', '2025-05-15 15:46:39', '2025-05-15 15:46:39');

-- ----------------------------
-- Table structure for stories
-- ----------------------------
DROP TABLE IF EXISTS `stories`;
CREATE TABLE `stories`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '故事ID',
  `title` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '故事标题 (接口中标题可能含HTML)',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '故事内容 (可能包含HTML)',
  `user_id` int NULL DEFAULT NULL COMMENT '创建用户ID (逻辑外键, 指向 users.id)',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2250 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '故事表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of stories
-- ----------------------------
INSERT INTO `stories` VALUES (1, '在我一生最好的黄金时代', '那一天我二十一岁，在我一生的黄金时代，我有好多奢望。我想爱，想吃，还想在一瞬间变成天上半明半暗的云。后来我才知道生活就是一个缓慢受锤的过程，人一天天老下去，奢望也一天天消失，最后变成了像挨了锤的牛一样。', 1, '2021-05-03 07:04:46');
INSERT INTO `stories` VALUES (2247, '我与地坛', '宇宙以其不息的欲望将一个歌舞炼为永恒。这欲望有怎样一个人间的姓名，大可忽略不计。', 1, '2025-05-11 13:24:39');
INSERT INTO `stories` VALUES (2248, '我与地坛', '宇宙以其不息的欲望将一个歌舞炼为永恒。这欲望有怎样一个人间的姓名，大可忽略不计。', 1, '2025-05-13 15:12:06');
INSERT INTO `stories` VALUES (2249, '大家加油', '相信我们都可以在这个不看好前端的时间点打拼出属于自己的成就!', 1, '2025-05-15 15:48:19');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名 (登录名)',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码 (应存储哈希值)',
  `realname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `cellphone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号码',
  `enable` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用: 1启用, 0禁用',
  `role_id` int NULL DEFAULT NULL COMMENT '角色ID (逻辑外键, 指向 roles.id)',
  `department_id` int NULL DEFAULT NULL COMMENT '部门ID (逻辑外键, 指向 departments.id)',
  `createAt` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateAt` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_user_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'coderwhy', '$2b$12$QFPFjS.0x/aMutx6KJgV.emrWfpGddKZNuwlpwre6I0P6AiA4cE/a', 'coderwhy', '18812345678', 1, 1, 1, '2021-01-02 10:20:26', '2025-05-16 18:25:21');
INSERT INTO `users` VALUES (2, '123', '$2b$12$PERNSbKtexUCnDc5nDe2buqoT8eW./4CXpWatnrMB./YkVnKXzlVu', '123', '13811111111', 1, 4, 2, '2025-05-16 18:45:14', '2025-05-16 18:45:14');
INSERT INTO `users` VALUES (3, 'miaozhiwen', '$2b$12$uOBFH6qVUDNdSKrEh66Ibe1vNGbrMGLTkQ3M8wBYnpGCxuXZhkfP2', 'Miaozhiwen', '13811111111', 1, 3, 2, '2025-05-16 18:46:38', '2025-05-16 18:46:38');

SET FOREIGN_KEY_CHECKS = 1;
