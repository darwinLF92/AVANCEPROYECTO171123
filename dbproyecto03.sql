-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 17-11-2023 a las 22:55:13
-- Versión del servidor: 1.0.428
-- Versión de PHP: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `dbproyecto03`
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=53 ;

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
(45, 'Can add venta', 12, 'add_venta'),
(46, 'Can change venta', 12, 'change_venta'),
(47, 'Can delete venta', 12, 'delete_venta'),
(48, 'Can view venta', 12, 'view_venta'),
(49, 'Can add detalle venta', 13, 'add_detalleventa'),
(50, 'Can change detalle venta', 13, 'change_detalleventa'),
(51, 'Can delete detalle venta', 13, 'delete_detalleventa'),
(52, 'Can view detalle venta', 13, 'view_detalleventa');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$PIrly0akFF4SJG9lvpjP9w$sr1k+onS7s2WbF9tvP0+71Sjr1cSoG3UTBBGnCSs34M=', '2023-11-15 14:51:26.000000', 1, 'Darwin', '', '', '', 1, 1, '2023-11-14 20:59:10.000000');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `clientes_cliente`
--

INSERT INTO `clientes_cliente` (`id`, `nit`, `nombre`, `direccion`, `telefono`, `correo`, `limitecredito`, `fecha_creacion`, `activo`, `saldo`) VALUES
(1, '12', 'ALEX VARGAS', 'Manzanotes, Zacapa', '41524152', 'alexv@gmail.com', '50000.00', '2023-11-14 21:18:55.000000', 1, '0.00'),
(2, '13', 'Hermanos Ovalle', 'Rio Hondo, Zacapa', '41524153', 'ovalle@gmail.com', '300000.00', '2023-11-14 21:19:18.000000', 1, '0.00');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=14 ;

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
(13, 'Ventas', 'detalleventa'),
(12, 'Ventas', 'venta');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=38 ;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'Clientes', '0001_initial', '2023-11-14 20:57:43.000000'),
(2, 'Clientes', '0002_cliente_saldo', '2023-11-14 20:57:43.000000'),
(3, 'Proveedor', '0001_initial', '2023-11-14 20:57:43.000000'),
(4, 'Producto', '0001_initial', '2023-11-14 20:57:43.000000'),
(5, 'Producto', '0002_producto_activo', '2023-11-14 20:57:43.000000'),
(6, 'Producto', '0003_rename_codigo_producto_codigo_and_more', '2023-11-14 20:57:43.000000'),
(7, 'Producto', '0004_producto_tiene_descuento', '2023-11-14 20:57:43.000000'),
(8, 'Producto', '0005_transaccion', '2023-11-14 20:57:43.000000'),
(9, 'Producto', '0006_alter_componenteproducto_producto_componente_and_more', '2023-11-14 20:57:43.000000'),
(10, 'Producto', '0007_producto_proveedor_producto_stock_minimo', '2023-11-14 20:57:44.000000'),
(11, 'Producto', '0008_alter_producto_stock', '2023-11-14 20:57:44.000000'),
(12, 'Producto', '0009_alter_componenteproducto_cantidad', '2023-11-14 20:57:44.000000'),
(13, 'Producto', '0010_alter_producto_precio_compra', '2023-11-14 20:57:44.000000'),
(14, 'Proveedor', '0002_proveedor_saldo', '2023-11-14 20:57:44.000000'),
(15, 'Ventas', '0001_initial', '2023-11-14 20:57:44.000000'),
(16, 'contenttypes', '0001_initial', '2023-11-14 20:57:44.000000'),
(17, 'auth', '0001_initial', '2023-11-14 20:57:44.000000'),
(18, 'admin', '0001_initial', '2023-11-14 20:57:45.000000'),
(19, 'admin', '0002_logentry_remove_auto_add', '2023-11-14 20:57:45.000000'),
(20, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-14 20:57:45.000000'),
(21, 'contenttypes', '0002_remove_content_type_name', '2023-11-14 20:57:45.000000'),
(22, 'auth', '0002_alter_permission_name_max_length', '2023-11-14 20:57:45.000000'),
(23, 'auth', '0003_alter_user_email_max_length', '2023-11-14 20:57:45.000000'),
(24, 'auth', '0004_alter_user_username_opts', '2023-11-14 20:57:45.000000'),
(25, 'auth', '0005_alter_user_last_login_null', '2023-11-14 20:57:45.000000'),
(26, 'auth', '0006_require_contenttypes_0002', '2023-11-14 20:57:45.000000'),
(27, 'auth', '0007_alter_validators_add_error_messages', '2023-11-14 20:57:45.000000'),
(28, 'auth', '0008_alter_user_username_max_length', '2023-11-14 20:57:45.000000'),
(29, 'auth', '0009_alter_user_last_name_max_length', '2023-11-14 20:57:45.000000'),
(30, 'auth', '0010_alter_group_name_max_length', '2023-11-14 20:57:45.000000'),
(31, 'auth', '0011_update_proxy_permissions', '2023-11-14 20:57:45.000000'),
(32, 'auth', '0012_alter_user_first_name_max_length', '2023-11-14 20:57:45.000000'),
(33, 'sessions', '0001_initial', '2023-11-14 20:57:45.000000'),
(34, 'Ventas', '0002_alter_venta_cliente', '2023-11-15 15:25:51.000000'),
(35, 'Ventas', '0003_alter_detalleventa_options_alter_venta_options_and_more', '2023-11-15 15:36:44.000000'),
(36, 'Ventas', '0004_alter_venta_fecha_creacion', '2023-11-15 20:16:35.000000'),
(37, 'Ventas', '0005_alter_venta_cambio_alter_venta_dias_credito_and_more', '2023-11-16 14:46:08.000000');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3mh813mulzv5nydopga1fjla9ieo5s8d', '.eJxVjDsOwjAUBO_iGln-Jc-mpOcM1tp-wQHkSPlUiLtDpBTQ7szsS0Rsa43bwnMcizgLLU6_W0J-cNtBuaPdJpmnts5jkrsiD7rI61T4eTncv4OKpX5rT5S6AQzKzoSssjIaKlkNJJ_J9711ngyMMs7x4EJnO2iwZXCwNIj3B-CGN8M:1r30Ve:bliYQlYACaHpzl1SzoGDyBerbkNiAi7pS-jEjJ9SU50', '2023-11-28 20:59:46.000000'),
('ek8fn8apeefguvwjjbloizpqf9lu3wq3', '.eJxVjDsOwjAUBO_iGln-Jc-mpOcM1tp-wQHkSPlUiLtDpBTQ7szsS0Rsa43bwnMcizgLLU6_W0J-cNtBuaPdJpmnts5jkrsiD7rI61T4eTncv4OKpX5rT5S6AQzKzoSssjIaKlkNJJ_J9711ngyMMs7x4EJnO2iwZXCwNIj3B-CGN8M:1r30de:DnCb6_PyQEWn1hmlLSzKFpjp7FzxGTgOy4PjRid1-xA', '2023-11-28 21:08:02.000000'),
('l5j0zgcs9o4hc39fi40bfh67pr8yjlrw', '.eJxVjDsOwjAUBO_iGln-Jc-mpOcM1tp-wQHkSPlUiLtDpBTQ7szsS0Rsa43bwnMcizgLLU6_W0J-cNtBuaPdJpmnts5jkrsiD7rI61T4eTncv4OKpX5rT5S6AQzKzoSssjIaKlkNJJ_J9711ngyMMs7x4EJnO2iwZXCwNIj3B-CGN8M:1r3HEk:r0QZwAweq4YCE6yl0XMbzXD2TNtqBC7D_oEZNGm0ddA', '2023-11-29 14:51:26.000000'),
('nwqf6foua7yc0oqbclzlk1pt917zpd6g', '.eJxVjDsOwjAUBO_iGln-Jc-mpOcM1tp-wQHkSPlUiLtDpBTQ7szsS0Rsa43bwnMcizgLLU6_W0J-cNtBuaPdJpmnts5jkrsiD7rI61T4eTncv4OKpX5rT5S6AQzKzoSssjIaKlkNJJ_J9711ngyMMs7x4EJnO2iwZXCwNIj3B-CGN8M:1r31lP:_4IPSZpPNwGzjl2ZuvSwIioHnI6tPk5If6N5Cw4GUI8', '2023-11-28 22:20:07.000000');

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `producto_componenteproducto`
--

INSERT INTO `producto_componenteproducto` (`id`, `cantidad`, `producto_componente_id`, `producto_principal_id`) VALUES
(1, '4.00', 3, 1),
(2, '3.00', 4, 1);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=5 ;

--
-- Volcado de datos para la tabla `producto_producto`
--

INSERT INTO `producto_producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `para_fabricacion`, `activo`, `tiene_descuento`, `proveedor_id`, `stock_minimo`) VALUES
(1, '1', 'NUCLEO CEBA 190 X 20KG', '', '63.4200', '250.00', '949.00', 1, 1, 1, NULL, 250),
(2, '2', 'Clortetraciclina 20% x 20kg', '', '800.0000', '1600.00', '10.00', 0, 1, 1, NULL, 4),
(3, '123', 'Bicarbonato de Sodio x 1 kilo', '', '4.8000', '7.50', '1500.00', 0, 1, 1, 1, 1000),
(4, '635', 'PVM Trouw Nutrition x 1 kilo', '', '14.7400', '22.50', '2250.00', 0, 1, 1, NULL, 1000);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `producto_transaccion`
--

INSERT INTO `producto_transaccion` (`id`, `cantidad`, `fecha_registro`, `producto_id`) VALUES
(1, 250, '2023-11-14 23:04:20.000000', 1);

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `proveedor_proveedor`
--

INSERT INTO `proveedor_proveedor` (`id`, `nit`, `nombre`, `direccion`, `telefono`, `correo`, `contacto`, `fecha_creacion`, `activo`, `saldo`) VALUES
(1, '123', 'Bretano Guatemala, S. A.', 'Guatemala', '41524152', 'bretano@gmail.com', 'Eva Arrivillaga', '2023-11-15 14:52:22.000000', 1, '0.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_detalleventa`
--

CREATE TABLE IF NOT EXISTS `ventas_detalleventa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stock` int(10) unsigned NOT NULL,
  `cantidad` int(10) unsigned NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `devolucion` tinyint(1) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  `venta_id` bigint(20) NOT NULL,
  `created` datetime(6) NOT NULL,
  `_order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Ventas_detalleventa_producto_id_080e2777_fk_Producto_producto_id` (`producto_id`),
  KEY `Ventas_detalleventa_venta_id_96b8ad61_fk_Ventas_venta_id` (`venta_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=27 ;

--
-- Volcado de datos para la tabla `ventas_detalleventa`
--

INSERT INTO `ventas_detalleventa` (`id`, `stock`, `cantidad`, `precio`, `descuento`, `subtotal`, `devolucion`, `producto_id`, `venta_id`, `created`, `_order`) VALUES
(1, 0, 1, '250.00', '0.00', '250.00', 0, 1, 1, '2023-11-15 15:36:44.000000', 0),
(2, 0, 300, '136.36', '0.00', '40908.00', 0, 1, 2, '2023-11-15 15:36:44.000000', 0),
(3, 0, 1, '1600.00', '0.00', '1600.00', 0, 2, 3, '2023-11-16 14:49:04.000000', 0),
(4, 0, 1, '250.00', '0.00', '250.00', 0, 1, 20, '2023-11-16 22:46:25.000000', 0),
(5, 0, 1, '250.00', '0.00', '250.00', 0, 1, 21, '2023-11-16 22:46:25.000000', 0),
(6, 0, 10, '1600.00', '0.00', '16000.00', 0, 2, 22, '2023-11-16 22:48:08.000000', 0),
(7, 0, 10, '250.00', '0.00', '2500.00', 0, 1, 22, '2023-11-16 22:48:08.000000', 0),
(8, 0, 10, '1600.00', '0.00', '16000.00', 0, 2, 23, '2023-11-16 22:48:08.000000', 0),
(9, 0, 10, '250.00', '0.00', '2500.00', 0, 1, 23, '2023-11-16 22:48:08.000000', 0),
(10, 0, 1, '1600.00', '0.00', '1600.00', 0, 2, 24, '2023-11-16 22:50:07.000000', 0),
(11, 0, 10, '1600.00', '0.00', '16000.00', 0, 2, 25, '2023-11-16 22:51:01.000000', 0),
(12, 0, 12, '7.50', '0.00', '90.00', 0, 3, 25, '2023-11-16 22:51:01.000000', 0),
(13, 0, 10, '22.50', '0.00', '225.00', 0, 4, 26, '2023-11-16 22:53:14.000000', 0),
(14, 0, 12, '250.00', '0.00', '3000.00', 0, 1, 27, '2023-11-17 16:03:58.000000', 0),
(15, 0, 10, '250.00', '0.00', '2500.00', 0, 1, 28, '2023-11-17 16:11:53.000000', 0),
(16, 0, 10, '1600.00', '0.00', '16000.00', 0, 2, 29, '2023-11-17 16:23:58.000000', 0),
(17, 0, 1, '1600.00', '0.00', '1600.00', 0, 2, 30, '2023-11-17 16:52:13.000000', 0),
(18, 0, 1, '1600.00', '0.00', '1600.00', 0, 2, 31, '2023-11-17 16:53:27.000000', 0),
(19, 0, 1, '250.00', '0.00', '250.00', 0, 1, 32, '2023-11-17 17:40:25.000000', 0),
(20, 0, 1, '1600.00', '0.00', '1600.00', 0, 2, 33, '2023-11-17 17:41:47.000000', 0),
(21, 0, 10, '250.00', '0.00', '2500.00', 0, 1, 34, '2023-11-17 17:50:44.000000', 0),
(22, 0, 30, '250.00', '1500.00', '6000.00', 0, 1, 35, '2023-11-17 20:03:17.000000', 0),
(23, 0, 300, '250.00', '34092.00', '40908.00', 0, 1, 36, '2023-11-17 20:05:29.000000', 0),
(24, 0, 3, '250.00', '0.00', '750.00', 0, 1, 37, '2023-11-17 21:14:00.000000', 0),
(25, 0, 2, '22.50', '0.00', '45.00', 0, 4, 37, '2023-11-17 21:14:00.000000', 0),
(26, 0, 1, '7.50', '0.00', '7.50', 0, 3, 37, '2023-11-17 21:14:00.000000', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_venta`
--

CREATE TABLE IF NOT EXISTS `ventas_venta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_creacion` date NOT NULL,
  `tipo_documento` varchar(7) NOT NULL,
  `tipo_pago` varchar(7) NOT NULL,
  `metodo_pago` varchar(8) DEFAULT NULL,
  `total` decimal(20,2) NOT NULL,
  `paga_con` decimal(10,2) DEFAULT NULL,
  `cambio` decimal(10,2) DEFAULT NULL,
  `comentarios` longtext DEFAULT NULL,
  `dias_credito` int(11) DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `cliente_id` bigint(20) DEFAULT NULL,
  `_order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Ventas_venta_cliente_id_c8ddb78b_fk_Clientes_cliente_id` (`cliente_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=38 ;

--
-- Volcado de datos para la tabla `ventas_venta`
--

INSERT INTO `ventas_venta` (`id`, `fecha_creacion`, `tipo_documento`, `tipo_pago`, `metodo_pago`, `total`, `paga_con`, `cambio`, `comentarios`, `dias_credito`, `fecha_vencimiento`, `cliente_id`, `_order`) VALUES
(1, '2023-11-14', 'envio', 'contado', 'efectivo', '500.00', '500.00', '0.00', '', 30, '2023-12-14', 1, 0),
(2, '2023-11-15', 'envio', 'credito', 'cheque', '40908.00', '40908.00', '0.00', 'EF-0001', 30, '2023-12-15', 2, 0),
(3, '2023-11-16', 'envio', 'credito', NULL, '1600.00', NULL, NULL, '', 30, '2023-12-16', 1, 0),
(4, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', '', 0, NULL, 1, 1),
(5, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', '', 0, NULL, 1, 2),
(6, '2023-11-16', 'envio', 'contado', 'efectivo', '3000.00', '0.00', '0.00', '', 0, NULL, 1, 3),
(7, '2023-11-16', 'envio', 'contado', 'efectivo', '3000.00', '0.00', '0.00', '', 0, NULL, 1, 4),
(8, '2023-11-16', 'envio', 'contado', 'efectivo', '16500.00', '0.00', '0.00', 'EF-2023', 0, NULL, 2, 5),
(9, '2023-11-16', 'envio', 'contado', 'efectivo', '16500.00', '0.00', '0.00', 'EF-2023', 0, NULL, 2, 5),
(10, '2023-11-16', 'envio', 'credito', 'efectivo', '250.00', '0.00', '0.00', 'prueba', 30, '2023-12-16', 1, 6),
(11, '2023-11-16', 'envio', 'credito', 'efectivo', '250.00', '0.00', '0.00', 'prueba', 30, '2023-12-16', 1, 7),
(12, '2023-11-16', 'envio', 'credito', 'efectivo', '6400.00', '0.00', '0.00', 'prueba2', 30, '2023-12-16', 2, 8),
(13, '2023-11-16', 'envio', 'credito', 'efectivo', '6400.00', '0.00', '0.00', 'prueba2', 30, '2023-12-16', 2, 9),
(14, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'fafaa', 0, NULL, NULL, 10),
(15, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'fafaa', 0, NULL, NULL, 10),
(16, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', NULL, NULL, 'fafafaf', NULL, NULL, 1, 11),
(17, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', NULL, NULL, 'fafafaf', NULL, NULL, 1, 12),
(18, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'fafafafaff', 0, NULL, 1, 13),
(19, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'fafafafaff', 0, NULL, 1, 13),
(20, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'afaffasfasf', 0, NULL, 1, 14),
(21, '2023-11-16', 'envio', 'contado', 'efectivo', '250.00', '0.00', '0.00', 'afaffasfasf', 0, NULL, 1, 15),
(22, '2023-11-16', 'envio', 'credito', 'efectivo', '18500.00', '0.00', '0.00', 'envio ovalle', 30, '2023-12-16', 2, 16),
(23, '2023-11-16', 'envio', 'credito', 'efectivo', '18500.00', '0.00', '0.00', 'envio ovalle', 30, '2023-12-16', 2, 17),
(24, '2023-11-16', 'envio', 'contado', 'efectivo', '1600.00', '0.00', '0.00', 'prueba2', 0, NULL, 1, 18),
(25, '2023-11-24', 'envio', 'contado', 'efectivo', '16090.00', '0.00', '0.00', 'prueba de venta', 0, NULL, 1, 0),
(26, '2023-11-16', 'factura', 'credito', 'efectivo', '225.00', '0.00', '0.00', 'prueba de venta online', 30, '2023-12-16', 1, 19),
(27, '2023-11-17', 'envio', 'credito', 'null', '3000.00', '0.00', '0.00', 'prueba pago', 30, '2023-12-17', 1, 0),
(28, '2023-11-17', 'envio', 'credito', NULL, '2500.00', '0.00', '0.00', 'prueba 17112023', 30, '2023-12-17', 1, 1),
(29, '2023-11-17', 'envio', 'contado', 'efectivo', '16000.00', '1600.00', '0.00', 'prueba venta pagos', 0, NULL, 1, 2),
(30, '2023-11-17', 'envio', 'contado', NULL, '1600.00', '0.00', '0.00', 'venta contado', NULL, NULL, 1, 3),
(31, '2023-11-17', 'envio', 'contado', 'efectivo', '1600.00', '2000.00', '400.00', 'venta contado con cambio', NULL, NULL, 1, 4),
(32, '2023-11-17', 'envio', 'contado', 'efectivo', '250.00', '400.00', '150.00', NULL, NULL, '2023-11-17', 1, 5),
(33, '2023-11-17', 'envio', 'credito', NULL, '1600.00', '0.00', '0.00', NULL, 30, NULL, 1, 6),
(34, '2023-11-17', 'envio', 'credito', NULL, '2500.00', '0.00', '0.00', 'prueba venta credito', 30, '2023-12-17', 1, 7),
(35, '2023-11-17', 'envio', 'contado', 'efectivo', '6000.00', '6100.00', '100.00', 'VENTA ITALO', NULL, NULL, 1, 8),
(36, '2023-11-17', 'envio', 'credito', NULL, '40908.00', '0.00', '0.00', 'VENTA OVALLE', 30, '2023-12-17', 2, 9),
(37, '2023-11-17', 'envio', 'contado', NULL, '802.50', '0.00', '0.00', 'pueba venta con busqueda', NULL, NULL, 1, 10);

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
-- Filtros para la tabla `producto_componenteproducto`
--
ALTER TABLE `producto_componenteproducto`
  ADD CONSTRAINT `Producto_componentep_producto_componente__a9705919_fk_Producto_` FOREIGN KEY (`producto_componente_id`) REFERENCES `producto_producto` (`id`),
  ADD CONSTRAINT `Producto_componentep_producto_principal_i_1da14157_fk_Producto_` FOREIGN KEY (`producto_principal_id`) REFERENCES `producto_producto` (`id`);

--
-- Filtros para la tabla `producto_producto`
--
ALTER TABLE `producto_producto`
  ADD CONSTRAINT `Producto_producto_proveedor_id_a52b4fdb_fk_Proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor_proveedor` (`id`);

--
-- Filtros para la tabla `producto_transaccion`
--
ALTER TABLE `producto_transaccion`
  ADD CONSTRAINT `Producto_transaccion_producto_id_36cd0fec_fk_Producto_` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`);

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
