class GatewayNotImplemented(Exception):
    pass

class BaseGateway:
    def procesar(self, payment):
        raise GatewayNotImplemented(f"{self.__class__.__name__} aún no está implementado")

class MercadoPagoGateway(BaseGateway):
    pass

class CuentaRutGateway(BaseGateway):
    pass

class PayPalGateway(BaseGateway):
    pass

class TarjetaDebitoGateway(BaseGateway):
    # Pago presencial, sin integración externa. Recepción marca aprobado manualmente.
    def procesar(self, payment):
        payment.estado = 'aprobado'
        payment.save()
        return payment

GATEWAYS = {
    'mercadopago': MercadoPagoGateway,
    'cuenta_rut': CuentaRutGateway,
    'paypal': PayPalGateway,
    'tarjeta_debito': TarjetaDebitoGateway,
}

def get_gateway(metodo_pago):
    gateway_class = GATEWAYS.get(metodo_pago)
    if not gateway_class:
        raise GatewayNotImplemented(f"Método {metodo_pago} desconocido")
    return gateway_class()