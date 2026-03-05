-- =====================
-- TABLAS PRINCIPALES
-- =====================

CREATE TABLE public.rol (
    id_rol SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_rol INT,
    nombre VARCHAR(100),
    contrasena_hash TEXT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol)
);


CREATE TABLE public.cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE public.direccion (
    id_direccion SERIAL PRIMARY KEY,
    id_cliente INT,
    descripcion VARCHAR(200),
    FOREIGN KEY (id_cliente) REFERENCES public.cliente(id_cliente)
);

CREATE TABLE public.estado (
    id_estado SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_direccion INT,
    id_estado INT,
    id_cliente INT,
    fecha_entrega TIMESTAMP,
    fecha_pedido TIMESTAMP,
    comentario VARCHAR(255),
    tipo_entrega BOOLEAN,
    subtotal NUMERIC(10,2),
    total NUMERIC(10,2),
    FOREIGN KEY (id_direccion) REFERENCES public.direccion(id_direccion),
    FOREIGN KEY (id_estado) REFERENCES public.estado(id_estado),
    FOREIGN KEY (id_cliente) REFERENCES public.cliente(id_cliente)
);

CREATE TABLE public.usuario_has_pedidos (
    id_usuario INT,
    id_pedido INT,
    PRIMARY KEY (id_usuario, id_pedido),
    FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario),
    FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido)
);

-- =====================
-- PAGOS
-- =====================

CREATE TABLE public.estado_pago (
    id_estado_pago SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.tipo_pago (
    id_tipo_pago SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.pago (
    id_pago SERIAL PRIMARY KEY,
    id_pedido INT,
    id_estado_pago INT,
    id_tipo_pago INT,
    anticipo BOOLEAN,
    monto NUMERIC(10,2),
    fecha TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido),
    FOREIGN KEY (id_estado_pago) REFERENCES public.estado_pago(id_estado_pago),
    FOREIGN KEY (id_tipo_pago) REFERENCES public.tipo_pago(id_tipo_pago)
);

-- =====================
-- RECETAS Y MATERIA PRIMA
-- =====================

CREATE TABLE public.unidad_medida (
    id_unidad SERIAL PRIMARY KEY,
    descripcion VARCHAR(100),
    abreviatura VARCHAR(10)
);

CREATE TABLE public.materia_prima (
    id_materia SERIAL PRIMARY KEY,
    id_unidad INT,
    descripcion VARCHAR(100),
    precio_unitario NUMERIC(10,2),
    minimo NUMERIC(10,2),
    maximo NUMERIC(10,2),
    stock_actual NUMERIC(10,2),
    imagen VARCHAR(255),
    activo BOOLEAN,
    FOREIGN KEY (id_unidad) REFERENCES public.unidad_medida(id_unidad)
);

CREATE TABLE public.receta (
    id_receta SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.receta_materia_prima (
    id_receta INT,
    id_materia INT,
    cantidad NUMERIC(10,2),
    PRIMARY KEY (id_receta, id_materia),
    FOREIGN KEY (id_receta) REFERENCES public.receta(id_receta),
    FOREIGN KEY (id_materia) REFERENCES public.materia_prima(id_materia)
);

-- =====================
-- PRODUCTOS
-- =====================

CREATE TABLE public.categoria (
    id_categoria SERIAL PRIMARY KEY,
    descripcion VARCHAR(100)
);

CREATE TABLE public.producto (
    id_producto SERIAL PRIMARY KEY,
    id_categoria INT,
    id_receta INT,
    descripcion VARCHAR(100),
    precio_unitario NUMERIC(10,2),
    imagen VARCHAR(255),
    activo BOOLEAN,
    FOREIGN KEY (id_categoria) REFERENCES public.categoria(id_categoria),
    FOREIGN KEY (id_receta) REFERENCES public.receta(id_receta)
);

CREATE TABLE public.pedidos_has_producto (
    id_pedido INT,
    id_producto INT,
    cantidad INT,
    precio_diseño NUMERIC(10,2),
    precio_envio NUMERIC(10,2),
    PRIMARY KEY (id_pedido, id_producto),
    FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES public.producto(id_producto)
);

-- =====================
-- COMPRAS
-- =====================

CREATE TABLE public.proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    descripcion VARCHAR(100),
    direccion VARCHAR(200),
    contacto VARCHAR(100)
);

CREATE TABLE public.compra (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT,
    fecha TIMESTAMP,
    total NUMERIC(10,2),
    FOREIGN KEY (id_proveedor) REFERENCES public.proveedor(id_proveedor)
);

CREATE TABLE public.materia_prima_compra (
    id_materia INT,
    id_compra INT,
    cantidad NUMERIC(10,2),
    precio_individual NUMERIC(10,2),
    PRIMARY KEY (id_materia, id_compra),
    FOREIGN KEY (id_materia) REFERENCES public.materia_prima(id_materia),
    FOREIGN KEY (id_compra) REFERENCES public.compra(id_compra)
);