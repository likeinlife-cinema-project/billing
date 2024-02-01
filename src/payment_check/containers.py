from dependency_injector import containers

from billing.containers import Container as BillingContainer


@containers.copy(BillingContainer)
class Container(containers.DeclarativeContainer):
    ...
