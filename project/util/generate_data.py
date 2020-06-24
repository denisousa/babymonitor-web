import random
from time import time

# Configuração:
# Máximo de repetições do status (bom)
# Probabilidade da criança ficar mal
# Tempo de confirmação do usuário para o celular
# O tempo para acudir a criança (Tempo de exibição da alerta na TV)


def configure_data(function):
    def wrapped(flag, time_called=0):
        # if flag is 'force_fine', it means we should generate a
        # data where the baby is all fine
        if flag == 'force_fine':
            wrapped.calls = 0
            max_no_changes = random.randint(3, 7)
            return function('force_fine', time_called=0)

        # if flag is 0, it means that a new status is generated.
        # according to the maximum repeating
        if flag == 'new_status':
            wrapped.calls += 1
            if wrapped.calls < max_no_changes:
                # if it is the first time the function is called
                # a new random status is generated
                # otherwise, the previous status is repeated
                if wrapped.calls == 1:
                    return function('new_status', time_called)
                return function('repeat_status', time_called)
            # if the maximum is reached,
            # a new random status is generated.
            else:
                wrapped.calls = 0
                max_no_changes = random.randint(3, 7)
                return function('new_status', time_called)

        # if flag is 1, it means that the previous
        # status should be repeated
        if flag == 'new_status':
            wrapped.calls += 1
            return function('repeat_status', time_called)

    max_no_changes = random.randint(3, 7)
    wrapped.calls = 0
    return wrapped


@configure_data
def data_from_baby(flag: str, time_called: time=time(), last_record: dict=None):
    data = {}

    if flag == 'force_fine':
        data['crying'] = False
        data['sleeping'] = random.choices([True, False], [0.75, 0.25], k=1)[0]
        data['breathing'] = True
        data['time_no_breathing'] = 0

    elif flag == 'new_status':
        data['crying'] = random.choices([True, False], [0.6, 0.4], k=1)[0]

        if data['crying']:
            data['sleeping'] = False
            data['breathing'] = True
            data['time_no_breathing'] = 0

        else:
            data['sleeping'] = random.choices([True, False], [0.75, 0.25], k=1)[0]
            data['breathing'] = random.choices([True, False], [0.25, 0.75], k=1)[0]

            if not data['breathing']:
                data["time_no_breathing"] += (time.time() - time_called) % 60

            else:
                data['time_no_breathing'] = 0

            if data['sleeping']:
                data['crying'] = False

    elif flag == 'repeat_status':
        # Fazer função para recuperar dados do banco
        # Para exemplo, fiz arquivo.
        data = last_record
        if not last_record["breathing"]:
            data["time_no_breathing"] += (time.time() - time_called) % 60
    
    return data
