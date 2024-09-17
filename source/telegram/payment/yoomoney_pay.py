from yoomoney import Quickpay
from yoomoney import Client

token = "4100116814239549.74B2540FC4A1AC464F861DCCD2BDAE27E52EB079961EC0E3281C796223702D9084A355600DA2FE838DDDC1EDF9622B9E6F116514EDB7D681B8C5ACF0D86D6F04A73ACB12A9773B76274D6409478AD0C5031D7579687504A1573778590CF780A236079E4DD8890F06E8EF2DC8A28A72A25317D57AA233BBE8DD56D607E15CFCB3"
client = Client(token)

def pay_yoomoney(user_id: str, check: int, id: int):
    quickpay = Quickpay(
                receiver="4100116814239549",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=check,
                label=f'{user_id}|{check}|{id}'
                )
    return quickpay.base_url


def check_pay_yoomoney(label: str):
    history = client.operation_history(label=label)

    for operation in history.operations:
        return operation.status
        # print()
        # print("Operation:", operation.operation_id)
        # print("\tStatus     -->", operation.status)
        # print("\tDatetime   -->", operation.datetime)
        # print("\tTitle      -->", operation.title)
        # print("\tPattern id -->", operation.pattern_id)
        # print("\tDirection  -->", operation.direction)
        # print("\tAmount     -->", operation.amount)
        # print("\tLabel      -->", operation.label)
        # print("\tType       -->", operation.type)





