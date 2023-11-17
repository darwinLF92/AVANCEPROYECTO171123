-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 10-11-2023 a las 22:58:38
-- Versión del servidor: 1.0.428
-- Versión de PHP: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `dbproyecto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=61 ;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add componente producto', 7, 'add_componenteproducto'),
(26, 'Can change componente producto', 7, 'change_componenteproducto'),
(27, 'Can delete componente producto', 7, 'delete_componenteproducto'),
(28, 'Can view componente producto', 7, 'view_componenteproducto'),
(29, 'Can add producto', 8, 'add_producto'),
(30, 'Can change producto', 8, 'change_producto'),
(31, 'Can delete producto', 8, 'delete_producto'),
(32, 'Can view producto', 8, 'view_producto'),
(33, 'Can add transaccion', 9, 'add_transaccion'),
(34, 'Can change transaccion', 9, 'change_transaccion'),
(35, 'Can delete transaccion', 9, 'delete_transaccion'),
(36, 'Can view transaccion', 9, 'view_transaccion'),
(37, 'Can add Proveedor', 10, 'add_proveedor'),
(38, 'Can change Proveedor', 10, 'change_proveedor'),
(39, 'Can delete Proveedor', 10, 'delete_proveedor'),
(40, 'Can view Proveedor', 10, 'view_proveedor'),
(41, 'Can add Cliente', 11, 'add_cliente'),
(42, 'Can change Cliente', 11, 'change_cliente'),
(43, 'Can delete Cliente', 11, 'delete_cliente'),
(44, 'Can view Cliente', 11, 'view_cliente'),
(45, 'Can add cliente', 12, 'add_cliente'),
(46, 'Can change cliente', 12, 'change_cliente'),
(47, 'Can delete cliente', 12, 'delete_cliente'),
(48, 'Can view cliente', 12, 'view_cliente'),
(49, 'Can add venta', 13, 'add_venta'),
(50, 'Can change venta', 13, 'change_venta'),
(51, 'Can delete venta', 13, 'delete_venta'),
(52, 'Can view venta', 13, 'view_venta'),
(53, 'Can add detalle venta', 14, 'add_detalleventa'),
(54, 'Can change detalle venta', 14, 'change_detalleventa'),
(55, 'Can delete detalle venta', 14, 'delete_detalleventa'),
(56, 'Can view detalle venta', 14, 'view_detalleventa'),
(57, 'Can add producto', 15, 'add_producto'),
(58, 'Can change producto', 15, 'change_producto'),
(59, 'Can delete producto', 15, 'delete_producto'),
(60, 'Can view producto', 15, 'view_producto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$r1dxelvsLuWYLkXCOSdPbF$8+w5l+giC7NHoAjBbpIfcocCV94h2pilV73ro3qg9TY=', '2023-11-09 19:58:08.000000', 1, 'Darwin', '', '', '', 1, 1, '2023-11-07 00:20:36.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes_cliente`
--

CREATE TABLE IF NOT EXISTS `clientes_cliente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nit` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `limitecredito` decimal(10,2) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `saldo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit` (`nit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `clientes_cliente`
--

INSERT INTO `clientes_cliente` (`id`, `nit`, `nombre`, `direccion`, `telefono`, `correo`, `limitecredito`, `fecha_creacion`, `activo`, `saldo`) VALUES
(1, '17966639', 'Karina Acevedo', 'Chiquimula', '475412521', 'karina@gmail.com', '1000.00', '2023-11-09 19:39:58.000000', 1, '0.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=16 ;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(11, 'Clientes', 'cliente'),
(5, 'contenttypes', 'contenttype'),
(7, 'Producto', 'componenteproducto'),
(8, 'Producto', 'producto'),
(9, 'Producto', 'transaccion'),
(10, 'Proveedor', 'proveedor'),
(6, 'sessions', 'session'),
(12, 'Ventas', 'cliente'),
(14, 'Ventas', 'detalleventa'),
(15, 'Ventas', 'producto'),
(13, 'Ventas', 'venta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=36 ;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'Producto', '0001_initial', '2023-11-07 00:19:12.000000'),
(2, 'Producto', '0002_producto_activo', '2023-11-07 00:19:12.000000'),
(3, 'Producto', '0003_rename_codigo_producto_codigo_and_more', '2023-11-07 00:19:12.000000'),
(4, 'Producto', '0004_producto_tiene_descuento', '2023-11-07 00:19:12.000000'),
(5, 'Producto', '0005_transaccion', '2023-11-07 00:19:12.000000'),
(6, 'contenttypes', '0001_initial', '2023-11-07 00:19:12.000000'),
(7, 'auth', '0001_initial', '2023-11-07 00:19:13.000000'),
(8, 'admin', '0001_initial', '2023-11-07 00:19:13.000000'),
(9, 'admin', '0002_logentry_remove_auto_add', '2023-11-07 00:19:13.000000'),
(10, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-07 00:19:13.000000'),
(11, 'contenttypes', '0002_remove_content_type_name', '2023-11-07 00:19:14.000000'),
(12, 'auth', '0002_alter_permission_name_max_length', '2023-11-07 00:19:14.000000'),
(13, 'auth', '0003_alter_user_email_max_length', '2023-11-07 00:19:14.000000'),
(14, 'auth', '0004_alter_user_username_opts', '2023-11-07 00:19:14.000000'),
(15, 'auth', '0005_alter_user_last_login_null', '2023-11-07 00:19:14.000000'),
(16, 'auth', '0006_require_contenttypes_0002', '2023-11-07 00:19:14.000000'),
(17, 'auth', '0007_alter_validators_add_error_messages', '2023-11-07 00:19:14.000000'),
(18, 'auth', '0008_alter_user_username_max_length', '2023-11-07 00:19:14.000000'),
(19, 'auth', '0009_alter_user_last_name_max_length', '2023-11-07 00:19:14.000000'),
(20, 'auth', '0010_alter_group_name_max_length', '2023-11-07 00:19:14.000000'),
(21, 'auth', '0011_update_proxy_permissions', '2023-11-07 00:19:14.000000'),
(22, 'auth', '0012_alter_user_first_name_max_length', '2023-11-07 00:19:14.000000'),
(23, 'sessions', '0001_initial', '2023-11-07 00:19:14.000000'),
(24, 'Producto', '0006_alter_componenteproducto_producto_componente_and_more', '2023-11-08 02:35:57.000000'),
(25, 'Proveedor', '0001_initial', '2023-11-09 18:06:09.000000'),
(26, 'Producto', '0007_producto_proveedor_producto_stock_minimo', '2023-11-09 18:46:05.000000'),
(27, 'Clientes', '0001_initial', '2023-11-09 19:36:33.000000'),
(28, 'Clientes', '0002_cliente_saldo', '2023-11-09 19:52:21.000000'),
(29, 'Proveedor', '0002_proveedor_saldo', '2023-11-09 19:52:21.000000'),
(31, 'Ventas', '0002_rename_precio_venta_detalleventa_precio_and_more', '2023-11-10 15:19:45.000000'),
(32, 'Ventas', '0001_initial', '2023-11-10 15:41:25.000000'),
(33, 'Producto', '0008_alter_producto_stock', '2023-11-10 20:57:45.000000'),
(34, 'Producto', '0009_alter_componenteproducto_cantidad', '2023-11-10 21:04:40.000000'),
(35, 'Producto', '0010_alter_producto_precio_compra', '2023-11-10 21:25:01.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('dtop3ac7knsqs4j8sicgtasyqa1i94gw', '.eJxVjEsKwzAMRO_idTG2RRK5y-57BiNZVpO2xJDPKvTuTSCLFmY1781sJtG69Gmdy5QGMVfjzeW3Y8qvMh5AnjQ-qs11XKaB7aHYk872XqW8b6f7d9DT3O9rYAmC2rYlRIYYKXTZNwhAvnEB9giw73KhDrGAsKrToJERAV1Q8_kC1n03pg:1r0XKa:f1zq19m1upbN9FvRRfaBjTFOc00amZeoDIoI8RkdeCc', '2023-11-22 01:26:08.000000'),
('hvobmjpur0vtfkljy9vcggnzb2r1u9zu', '.eJxVjEsKwzAMRO_idTG2RRK5y-57BiNZVpO2xJDPKvTuTSCLFmY1781sJtG69Gmdy5QGMVfjzeW3Y8qvMh5AnjQ-qs11XKaB7aHYk872XqW8b6f7d9DT3O9rYAmC2rYlRIYYKXTZNwhAvnEB9giw73KhDrGAsKrToJERAV1Q8_kC1n03pg:1r0o9b:oZ5XcCaOO3FQKHSeFzHgpt30N60jqq_W32adkt4Gi8E', '2023-11-22 19:23:55.000000'),
('ne0fzagqr2rsq37093lr60fdy4lmlfpo', '.eJxVjEsKwzAMRO_idTG2RRK5y-57BiNZVpO2xJDPKvTuTSCLFmY1781sJtG69Gmdy5QGMVfjzeW3Y8qvMh5AnjQ-qs11XKaB7aHYk872XqW8b6f7d9DT3O9rYAmC2rYlRIYYKXTZNwhAvnEB9giw73KhDrGAsKrToJERAV1Q8_kC1n03pg:1r1BAG:7eaNa18S8mCr4S0fEozdVMdJpOCtI7TCQxh4g4Do8l8', '2023-11-23 19:58:08.000000'),
('wjttg1xl6hy944h7yxei9zp6bkltfnks', '.eJxVjEsKwzAMRO_idTG2RRK5y-57BiNZVpO2xJDPKvTuTSCLFmY1781sJtG69Gmdy5QGMVfjzeW3Y8qvMh5AnjQ-qs11XKaB7aHYk872XqW8b6f7d9DT3O9rYAmC2rYlRIYYKXTZNwhAvnEB9giw73KhDrGAsKrToJERAV1Q8_kC1n03pg:1r193e:kosD4GpADjqI2LqsUnXPQP-miWCwDE6ielJqfHMU6Wo', '2023-11-23 17:43:10.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_componenteproducto`
--

CREATE TABLE IF NOT EXISTS `producto_componenteproducto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cantidad` decimal(10,2) NOT NULL,
  `producto_componente_id` bigint(20) NOT NULL,
  `producto_principal_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Producto_componentep_producto_componente__a9705919_fk_Producto_` (`producto_componente_id`),
  KEY `Producto_componentep_producto_principal_i_1da14157_fk_Producto_` (`producto_principal_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=35 ;

--
-- Volcado de datos para la tabla `producto_componenteproducto`
--

INSERT INTO `producto_componenteproducto` (`id`, `cantidad`, `producto_componente_id`, `producto_principal_id`) VALUES
(1, '2.00', 2, 1),
(2, '2.00', 2, 3),
(3, '2.00', 3, 2),
(4, '3.00', 2, 4),
(5, '2.00', 3, 4),
(6, '4.00', 1, 4),
(7, '2.00', 1, 7),
(8, '3.00', 1, 8),
(9, '3.00', 9, 11),
(14, '2.00', 9, 13),
(15, '3.00', 10, 13),
(18, '8.00', 10, 11),
(19, '3.00', 12, 11),
(29, '10.73', 15, 20),
(30, '4.00', 14, 20),
(31, '3.00', 17, 20),
(32, '2.00', 16, 20),
(33, '0.23', 18, 20),
(34, '0.04', 19, 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_producto`
--

CREATE TABLE IF NOT EXISTS `producto_producto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `precio_compra` decimal(10,4) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` decimal(10,2) NOT NULL,
  `para_fabricacion` tinyint(1) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `tiene_descuento` tinyint(1) NOT NULL,
  `proveedor_id` bigint(20) DEFAULT NULL,
  `stock_minimo` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `CODIGO` (`codigo`),
  KEY `Producto_producto_proveedor_id_a52b4fdb_fk_Proveedor` (`proveedor_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=21 ;

--
-- Volcado de datos para la tabla `producto_producto`
--

INSERT INTO `producto_producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `para_fabricacion`, `activo`, `tiene_descuento`, `proveedor_id`, `stock_minimo`) VALUES
(9, '6363', 'PRODUCTO 1', '', '4.8000', '6.00', '270.00', 0, 1, 1, NULL, 0),
(10, '6364411', 'PRODUCTO 2', '', '6.5000', '8.50', '220.00', 0, 1, 1, NULL, 0),
(11, '741', 'NUCLEO', '', '85.9000', '250.00', '10.00', 1, 1, 1, NULL, 0),
(12, '963', 'PRODUCTO 3', '', '6.5000', '9.50', '220.00', 0, 1, 1, NULL, 0),
(13, '963554', 'PRUEBA', '', '94.5000', '250.00', '0.00', 1, 1, 1, NULL, 0),
(14, '1', 'Bicarbonato x 1 kilo', '', '4.5200', '6.50', '880.00', 0, 1, 1, NULL, 1000),
(15, '2', 'Carbonato de calcio x 1kilo', '', '0.5600', '1.25', '21813.10', 0, 1, 1, NULL, 10000),
(16, '3', 'Sal Refinada Industrial x 1kilo', '', '2.2000', '3.50', '3476.00', 0, 1, 1, NULL, 2000),
(17, '6', 'Pvm ganado trouw x 1 kilo', '', '14.7400', '22.00', '1410.00', 0, 1, 1, NULL, 1000),
(18, '9', 'Monensina Sodica x 1 kilo', '', '49.0000', '70.00', '378.10', 0, 1, 1, 2, 200),
(19, '63', 'Apetenzima Fresa x 1 kilo', '', '82.0000', '100.00', '78.80', 0, 1, 1, NULL, 20),
(20, '9634', 'NUCLEO CEBA 190 X 20KG', '', '87.2588', '250.00', '530.00', 1, 1, 1, NULL, 500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_transaccion`
--

CREATE TABLE IF NOT EXISTS `producto_transaccion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cantidad` int(11) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Producto_transaccion_producto_id_36cd0fec_fk_Producto_` (`producto_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci AUTO_INCREMENT=8 ;

--
-- Volcado de datos para la tabla `producto_transaccion`
--

INSERT INTO `producto_transaccion` (`id`, `cantidad`, `fecha_registro`, `producto_id`) VALUES
(1, 1, '2023-11-07 02:35:09.000000', 2),
(2, 25, '2023-11-07 04:22:11.000000', 4),
(3, 10, '2023-11-08 17:40:41.000000', 4),
(4, 10, '2023-11-10 21:10:48.000000', 11),
(5, 200, '2023-11-10 21:29:47.000000', 20),
(6, 250, '2023-11-10 21:31:15.000000', 20),
(7, 80, '2023-11-10 21:39:43.000000', 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor_proveedor`
--

CREATE TABLE IF NOT EXISTS `proveedor_proveedor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nit` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contacto` varchar(100) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `saldo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit` (`nit`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `proveedor_proveedor`
--

INSERT INTO `proveedor_proveedor` (`id`, `nit`, `nombre`, `direccion`, `telefono`, `correo`, `contacto`, `fecha_creacion`, `activo`, `saldo`) VALUES
(1, '89728335', 'Darwin Lopez', 'Aldea El Ingeniero', '48111688', 'estuardo.darwinlopez@gmail.com', 'Darwin Lopez', '2023-11-09 18:28:58.000000', 1, '0.00'),
(2, '63541', 'CORPORACION QUIRSA', 'GUATEMALA', '225211225', 'quirsa@gmail.com', 'Lisbeth Cardenas', '2023-11-10 21:33:50.000000', 1, '0.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_detalleventa`
--

CREATE TABLE IF NOT EXISTS `ventas_detalleventa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cantidad` int(11) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `producto_id` bigint(20) DEFAULT NULL,
  `venta_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Ventas_detalleventa_producto_id_080e2777_fk_Producto_producto_id` (`producto_id`),
  KEY `Ventas_detalleventa_venta_id_96b8ad61_fk_Ventas_venta_id` (`venta_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_venta`
--

CREATE TABLE IF NOT EXISTS `ventas_venta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` datetime(6) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Ventas_venta_cliente_id_c8ddb78b_fk_Clientes_cliente_id` (`cliente_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `producto_producto`
--
ALTER TABLE `producto_producto`
  ADD CONSTRAINT `Producto_producto_proveedor_id_a52b4fdb_fk_Proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor_proveedor` (`id`);

--
-- Filtros para la tabla `ventas_detalleventa`
--
ALTER TABLE `ventas_detalleventa`
  ADD CONSTRAINT `Ventas_detalleventa_producto_id_080e2777_fk_Producto_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`),
  ADD CONSTRAINT `Ventas_detalleventa_venta_id_96b8ad61_fk_Ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas_venta` (`id`);

--
-- Filtros para la tabla `ventas_venta`
--
ALTER TABLE `ventas_venta`
  ADD CONSTRAINT `Ventas_venta_cliente_id_c8ddb78b_fk_Clientes_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
