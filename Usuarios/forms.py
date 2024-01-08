from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserEditForm(forms.ModelForm):
    #diccionario para los permisos de usuarios
    SPANISH_PERMISSIONS = {
    'admin | log entry | Can add log entry': 'Administrador | Registro de actividad | Puede agregar entrada de registro',
    'admin | log entry | Can change log entry': 'Administrador | Registro de actividad | Puede cambiar entrada de registro',
    'admin | log entry | Can delete log entry': 'Administrador | Registro de actividad | Puede eliminar entrada de registro',
    'admin | log entry | Can view log entry': 'Administrador | Registro de actividad | Puede ver entrada de registro',
    
    'auth | group | Can add group': 'Autenticación | Grupo | Puede agregar grupo',
    'auth | group | Can change group': 'Autenticación | Grupo | Puede cambiar grupo',
    'auth | group | Can delete group': 'Autenticación | Grupo | Puede eliminar grupo',
    'auth | group | Can view group': 'Autenticación | Grupo | Puede ver grupo',
    
    'auth | permission | Can add permission': 'Autenticación | Permiso | Puede agregar permiso',
    'auth | permission | Can change permission': 'Autenticación | Permiso | Puede cambiar permiso',
    'auth | permission | Can delete permission': 'Autenticación | Permiso | Puede eliminar permiso',
    'auth | permission | Can view permission': 'Autenticación | Permiso | Puede ver permiso',
    
    'auth | user | Can add user': 'Autenticación | Usuario | Puede agregar usuario',
    'auth | user | Can change user': 'Autenticación | Usuario | Puede cambiar usuario',
    'auth | user | Can delete user': 'Autenticación | Usuario | Puede eliminar usuario',
    'auth | user | Can view user': 'Autenticación | Usuario | Puede ver usuario',
    
    'Clientes | cliente | Can add Cliente': 'Clientes | Cliente | Puede agregar cliente',
    'Clientes | cliente | Can change Cliente': 'Clientes | Cliente | Puede cambiar cliente',
    'Clientes | cliente | Can delete Cliente': 'Clientes | Cliente | Puede eliminar cliente',
    'Clientes | cliente | Can view Cliente': 'Clientes | Cliente | Puede ver cliente',
    
    'configuracion | configuracion | Can add configuracion': 'Configuración | Configuración | Puede agregar configuración',
    'configuracion | configuracion | Can change configuracion': 'Configuración | Configuración | Puede cambiar configuración',
    'configuracion | configuracion | Can delete configuracion': 'Configuración | Configuración | Puede eliminar configuración',
    'configuracion | configuracion | Can view configuracion': 'Configuración | Configuración | Puede ver configuración',
    
    'configuraciontienda | Can add ConfiguracionTienda': 'Configuración de Tienda | Puede agregar Configuración de Tienda',
    'configuraciontienda | Can change ConfiguracionTienda': 'Configuración de Tienda | Puede cambiar Configuración de Tienda',
    'configuraciontienda | Can delete ConfiguracionTienda': 'Configuración de Tienda | Puede eliminar Configuración de Tienda',
    'configuraciontienda | Can view ConfiguracionTienda': 'Configuración de Tienda | Puede ver Configuración de Tienda',
    
    'contenttypes | content type | Can add content type': 'Tipos de contenido | Tipo de contenido | Puede agregar tipo de contenido',
    'contenttypes | content type | Can change content type': 'Tipos de contenido | Tipo de contenido | Puede cambiar tipo de contenido',
    'contenttypes | content type | Can delete content type': 'Tipos de contenido | Tipo de contenido | Puede eliminar tipo de contenido',
    'contenttypes | content type | Can view content type': 'Tipos de contenido | Tipo de contenido | Puede ver tipo de contenido',
    
    'Producto | componente producto | Can add componente producto': 'Producto | Componente de producto | Puede agregar componente de producto',
    'Producto | componente producto | Can change componente producto': 'Producto | Componente de producto | Puede cambiar componente de producto',
    'Producto | componente producto | Can delete componente producto': 'Producto | Componente de producto | Puede eliminar componente de producto',
    'Producto | componente producto | Can view componente producto': 'Producto | Componente de producto | Puede ver componente de producto',
    
    'Producto | producto | Can add producto': 'Producto | Producto | Puede agregar producto',
    'Producto | producto | Can change producto': 'Producto | Producto | Puede cambiar producto',
    'Producto | producto | Can delete producto': 'Producto | Producto | Puede eliminar producto',
    'Producto | producto | Can view producto': 'Producto | Producto | Puede ver producto',
    
    'Producto | transaccion | Can add transaccion': 'Producto | Transacción | Puede agregar transacción',
    'Producto | transaccion | Can change transaccion': 'Producto | Transacción | Puede cambiar transacción',
    'Producto | transaccion | Can delete transaccion': 'Producto | Transacción | Puede eliminar transacción',
    'Producto | transaccion | Can view transaccion': 'Producto | Transacción | Puede ver transacción',
    
    'Proveedor | Proveedor | Can add Proveedor': 'Proveedor | Proveedor | Puede agregar proveedor',
    'Proveedor | Proveedor | Can change Proveedor': 'Proveedor | Proveedor | Puede cambiar proveedor',
    'Proveedor | Proveedor | Can delete Proveedor': 'Proveedor | Proveedor | Puede eliminar proveedor',
    'Proveedor | Proveedor | Can view Proveedor': 'Proveedor | Proveedor | Puede ver proveedor',
    
    'sessions | session | Can add session': 'Sesiones | Sesión | Puede agregar sesión',
    'sessions | session | Can change session': 'Sesiones | Sesión | Puede cambiar sesión',
    'sessions | session | Can delete session': 'Sesiones | Sesión | Puede eliminar sesión',
    'sessions | session | Can view session': 'Sesiones | Sesión | Puede ver sesión',
    
    'Vendedor | vendedor | Can add vendedor': 'Vendedor | Vendedor | Puede agregar vendedor',
    'Vendedor | vendedor | Can change vendedor': 'Vendedor | Vendedor | Puede cambiar vendedor',
    'Vendedor | vendedor | Can delete vendedor': 'Vendedor | Vendedor | Puede eliminar vendedor',
    'Vendedor | vendedor | Can view vendedor': 'Vendedor | Vendedor | Puede ver vendedor',
    
    'Ventas | anulacion | Can add anulacion': 'Ventas | Anulación | Puede agregar anulación',
    'Ventas | anulacion | Can change anulacion': 'Ventas | Anulación | Puede cambiar anulación',
    'Ventas | anulacion | Can delete anulacion': 'Ventas | Anulación | Puede eliminar anulación',
    'Ventas | anulacion | Can view anulacion': 'Ventas | Anulación | Puede ver anulación',
    
    'Ventas | anulacion cobro | Can add anulacion cobro': 'Ventas | Anulación de cobro | Puede agregar anulación de cobro',
    'Ventas | anulacion cobro | Can change anulacion cobro': 'Ventas | Anulación de cobro | Puede cambiar anulación de cobro',
    'Ventas | anulacion cobro | Can delete anulacion cobro': 'Ventas | Anulación de cobro | Puede eliminar anulación de cobro',
    'Ventas | anulacion cobro | Can view anulacion cobro': 'Ventas | Anulación de cobro | Puede ver anulación de cobro',
    
    'Ventas | cobro | Can add cobro': 'Ventas | Cobro | Puede agregar cobro',
    'Ventas | cobro | Can change cobro': 'Ventas | Cobro | Puede cambiar cobro',
    'Ventas | cobro | Can delete cobro': 'Ventas | Cobro | Puede eliminar cobro',
    'Ventas | cobro | Can view cobro': 'Ventas | Cobro | Puede ver cobro',
    
    'Ventas | detalle venta | Can add detalle venta': 'Ventas | Detalle de venta | Puede agregar detalle de venta',
    'Ventas | detalle venta | Can change detalle venta': 'Ventas | Detalle de venta | Puede cambiar detalle de venta',
    'Ventas | detalle venta | Can delete detalle venta': 'Ventas | Detalle de venta | Puede eliminar detalle de venta',
    'Ventas | detalle venta | Can view detalle venta': 'Ventas | Detalle de venta | Puede ver detalle de venta',
    
    'Ventas | devolucion | Can add devolucion': 'Ventas | Devolución | Puede agregar devolución',
    'Ventas | devolucion | Can change devolucion': 'Ventas | Devolución | Puede cambiar devolución',
    'Ventas | devolucion | Can delete devolucion': 'Ventas | Devolución | Puede eliminar devolución',
    'Ventas | devolucion | Can view devolucion': 'Ventas | Devolución | Puede ver devolución',
    
    'Ventas | venta | Can add venta': 'Ventas | Venta | Puede agregar venta',
    'Ventas | venta | Can change venta': 'Ventas | Venta | Puede cambiar venta',
    'Ventas | venta | Can delete venta': 'Ventas | Venta | Puede eliminar venta',
    'Ventas | venta | Can view venta': 'Ventas | Venta | Puede ver venta',
}

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_permissions']
    
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        
        translated_permissions = [
            (str(perm.id), self.SPANISH_PERMISSIONS.get(str(perm), str(perm))) for perm in Permission.objects.all()
        ]

        self.fields['user_permissions'].choices = translated_permissions
