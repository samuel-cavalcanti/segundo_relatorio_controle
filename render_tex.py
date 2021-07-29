import os


def load_tamplate(tamplate_path: str) -> str:
    try:
        with open(tamplate_path, 'r') as file:
            return file.read()
    except:
        print(f'Unable to load {tamplate_path}')
        exit(1)


def render_template(variables: dict, tamplate: str) -> str:
    renderized_tamplate = tamplate
    for key in variables:
        renderized_tamplate = renderized_tamplate.replace(
            f'%{key}%', variables[key])

    return renderized_tamplate


def add_type_k_latex(type_k: str, value, is_master=True) -> str:
    if is_master:
        result = '''K_{%TYPE%_{\\textrm{mestre}}}=%VALUE%'''.replace(
            '%TYPE%', type_k)
    else:
        result = '''K_{%TYPE%_{\\textrm{escravo}}}=%VALUE%'''.replace(
            '%TYPE%', type_k)

    return result.replace('%VALUE%', str(value))


def build_controller_figures_tex(master_controller: str, slave_controller: str, figure_names: list, captions: list) -> str:
    load_figure_tamplate_variables = {
        'MASTER_CONTROLLLER': master_controller,
        'SLAVE_CONTROLLER': slave_controller,
        'FILE_NAME': 'None',
        'MATH_CAPTION': 'None'
    }

    renderized_tamplates = list()
    load_figure_tamplate = load_tamplate('tamplates/load_figure_tampate.tex')

    for figure_name, caption in zip(figure_names, captions):
        load_figure_tamplate_variables['FILE_NAME'] = figure_name
        load_figure_tamplate_variables['MATH_CAPTION'] = caption

        renderized_tamplates += render_template(
            load_figure_tamplate_variables, load_figure_tamplate) + '\n'

    return ''.join(renderized_tamplates)


def build_main_tex(master_controller, master_result_dir, p_controller_figures_name, p_controller_captions, pd_controller_figures_name, pd_controller_captions, pi_controller_figures_name, pi_controller_captions, pid_controller_figures_name, pid_controller_captions, dev_pid_controller_figures_name, dev_pid_controller_captions, windup_pid_controller_figures_name, windup_pid_controller_captions):
    p_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'P', p_controller_figures_name, p_controller_captions)

    pd_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'PD', pd_controller_figures_name, pd_controller_captions)

    pi_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'PI', pi_controller_figures_name, pi_controller_captions)

    pid_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'PID', pid_controller_figures_name, pid_controller_captions)

    dev_pid_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'PID filtro derivativo', dev_pid_controller_figures_name, dev_pid_controller_captions)

    windup_pid_controller_figures_tex = build_controller_figures_tex(
        master_controller, 'PID filtro windup', windup_pid_controller_figures_name, windup_pid_controller_captions)

    main_tamplate_variables = {
        'CURRENT_MASTER': master_controller,
        'MASTER_DIR': master_result_dir,
        'SLAVE_P_CONTROLLER_FIGURES': p_controller_figures_tex,
        'SLAVE_PD_CONTROLLER_FIGURES': pd_controller_figures_tex,
        'SLAVE_PI_CONTROLLER_FIGURES': pi_controller_figures_tex,
        'SLAVE_PID_CONTROLLER_FIGURES': pid_controller_figures_tex,
        'SLAVE_DEV_PID_CONTROLLER_FIGURES': dev_pid_controller_figures_tex,
        'SLAVE_WINDUP_PID_CONTROLLER_FIGURES': windup_pid_controller_figures_tex
    }
    main_tamplate = load_tamplate('tamplates/main_tamplate.tex')
    main_tex = render_template(main_tamplate_variables, main_tamplate)
    return main_tex


def render_master_pi():
    master_controller = 'PI'
    master_result_dir = 'mestre_PI'
    p_controller_figures_name = [
        'Kp_master_500_Ki_master_2_Kp_slave_500',
        'Kp_master_500_Ki_master_20_Kp_slave_500',
        'Kp_master_500_Ki_master_50_Kp_slave_500'
    ]

    p_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 2)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 20)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 50)} \\quad {add_type_k_latex('p',500,is_master=False)}"
    ]

    pd_controller_figures_name = [
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Kd_slave_10000',
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Kd_slave_1000',
        'Kp_master_500_Ki_master_2_Kp_slave_500_Kd_slave_300'
    ]

    pd_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',1000,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 2)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',300,is_master=False)}"
    ]

    pi_controller_figures_name = [
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_0_5',
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_1',
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_5'
    ]

    pi_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',1,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',5,is_master=False)}"
    ]

    pid_controller_figures_name = [
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_0_5_Kd_slave_10000',
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_0_5_Kd_slave_1000',
        'Kp_master_500_Ki_master_0_5_Kp_slave_500_Ki_slave_0_5_Kd_slave_500'

    ]

    pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',10000,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',1000,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 0.5)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',500,is_master=False)}"
    ]

    dev_pid_controller_figures_name = [
        'Kp_master_500_Ki_master_2_Kp_slave_500_Ki_slave_0_5_Kd_slave_10000_Kn_slave_1',
        'Kp_master_500_Ki_master_2_Kp_slave_500_Ki_slave_0_5_Kd_slave_10000_Kn_slave_2',
        'Kp_master_500_Ki_master_30_Kp_slave_500_Ki_slave_0_5_Kd_slave_10000_Kn_slave_4_5'
    ]

    dev_pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 2)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',1,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 2)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',4.5,is_master=False)}"
    ]

    windup_pid_controller_figures_name = [
        'Kp_master_500_Ki_master_200_Kp_slave_500_Ki_slave_0_5_Kd_slave_45_Kaw_slave_2',
        'Kp_master_500_Ki_master_300_Kp_slave_500_Ki_slave_0_5_Kd_slave_45_Kaw_slave_2',
        'Kp_master_500_Ki_master_300_Kp_slave_500_Ki_slave_0_5_Kd_slave_45_Kaw_slave_5'
    ]

    windup_pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 200)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',45,is_master=False)} \\quad {add_type_k_latex('aw',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 300)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',45,is_master=False)} \\quad {add_type_k_latex('aw',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 300)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',45,is_master=False)} \\quad {add_type_k_latex('aw',5,is_master=False)}"
    ]

    main_tex = build_main_tex(master_controller, master_result_dir, p_controller_figures_name, p_controller_captions, pd_controller_figures_name, pd_controller_captions, pi_controller_figures_name,
                              pi_controller_captions, pid_controller_figures_name, pid_controller_captions, dev_pid_controller_figures_name, dev_pid_controller_captions, windup_pid_controller_figures_name, windup_pid_controller_captions)

    print(main_tex)


def render_master_pid():
    master_controller = 'PID'
    master_result_dir = 'mestre_PID'

    p_controller_figures_name = [
        'Kp_master_500_Ki_master_1_Kd_master_1_Kp_slave_500',
        'Kp_master_500_Ki_master_1_Kd_master_500_Kp_slave_500',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500'
    ]

    p_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 2)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p',500,is_master=False)}"
    ]

    pd_controller_figures_name = [
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Kd_slave_2',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Kd_slave_5',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Kd_slave_10'
    ]

    pd_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)}\\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',5,is_master=False)}"
    ]

    pi_controller_figures_name = [
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_5',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_10',
        'Kp_master_500_Ki_master_30_Kd_master_10000_Kp_slave_500_Ki_slave_0_5'
    ]

    pi_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',5,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',10,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 10000)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)}"
    ]

    pid_controller_figures_name = [
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_2',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_5',
        'Kp_master_500_Ki_master_30_Kd_master_10000_Kp_slave_500_Ki_slave_0_5_Kd_slave_1'

    ]

    pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',5,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 10000)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \quad {add_type_k_latex('d',1,is_master=False)}"
    ]

    dev_pid_controller_figures_name = [
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_5_Kn_slave_1',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_5_Kn_slave_2',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_5_Kn_slave_3'
    ]

    dev_pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',1,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',10000,is_master=False)} \\quad {add_type_k_latex('n',3,is_master=False)}"
    ]

    windup_pid_controller_figures_name = [
        'Kp_master_500_Ki_master_5_Kd_master_500_Kp_slave_500_Ki_slave_5_Kd_slave_1_Kaw_slave_0_005',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_0_5_Kd_slave_5_Kaw_slave_0_005',
        'Kp_master_500_Ki_master_30_Kd_master_500_Kp_slave_500_Ki_slave_30_Kd_slave_1_Kaw_slave_0_005'
    ]

    windup_pid_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 5)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',5,is_master=False)} \\quad {add_type_k_latex('d',1,is_master=False)} \\quad {add_type_k_latex('aw',0.005,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',0.5,is_master=False)} \\quad {add_type_k_latex('d',5,is_master=False)} \\quad {add_type_k_latex('aw',0.005,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 30)} \\quad {add_type_k_latex('d', 500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',30,is_master=False)} \\quad {add_type_k_latex('d',1,is_master=False)} \\quad {add_type_k_latex('aw',0.005,is_master=False)}"
    ]

    main_tex = build_main_tex(master_controller, master_result_dir, p_controller_figures_name, p_controller_captions, pd_controller_figures_name, pd_controller_captions, pi_controller_figures_name,
                              pi_controller_captions, pid_controller_figures_name, pid_controller_captions, dev_pid_controller_figures_name, dev_pid_controller_captions, windup_pid_controller_figures_name, windup_pid_controller_captions)

    print(main_tex)


def render_master_dev_pid():
    master_controller = 'PID filtro derivativo'
    master_result_dir = 'mestre_PID_filtro_derivativo'

    p_controller_figures_name = [
        'Kp_master_500_Ki_master_1_Kd_master_1_Kn_master_1_Kp_slave_500',
        'Kp_master_500_Ki_master_7_Kd_master_1_Kn_master_200_Kp_slave_500',
        'Kp_master_500_Ki_master_7_Kd_master_1_Kn_master_500_Kp_slave_500'
    ]

    p_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',1)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 7)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',200)} \\quad {add_type_k_latex('p',500,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 7)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p',500,is_master=False)}"
    ]

    pd_controller_figures_name = [
        'Kp_master_500_Ki_master_100_Kd_master_1_Kn_master_500_Kp_slave_500_Kd_slave_2',
        'Kp_master_500_Ki_master_100_Kd_master_1_Kn_master_500_Kp_slave_500_Kd_slave_3',
        'Kp_master_500_Ki_master_100_Kd_master_1_Kn_master_500_Kp_slave_500_Kd_slave_5'
    ]

    pd_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 100)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',2,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 100)}\\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',3,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 100)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('d',5,is_master=False)}"
    ]

    pi_controller_figures_name = [
        'Kp_master_500_Ki_master_1_Kd_master_1_Kn_master_750_Kp_slave_500_Ki_slave_14',
        'Kp_master_500_Ki_master_3_Kd_master_1_Kn_master_500_Kp_slave_500_Ki_slave_3',
        'Kp_master_500_Ki_master_7_Kd_master_1_Kn_master_500_Kp_slave_500_Ki_slave_3'
    ]

    pi_controller_captions = [
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',750)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',14,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 3)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',3,is_master=False)}",
        f"{add_type_k_latex('p', 500)} \\quad {add_type_k_latex('i', 7)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',500)} \\quad {add_type_k_latex('p', 500,is_master=False)} \\quad {add_type_k_latex('i',3,is_master=False)}"
    ]

    pid_controller_figures_name = [
        'Kp_master_2000_Ki_master_4_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_4_Kd_slave_1',
        'Kp_master_2000_Ki_master_4_Kd_master_1_Kn_master_200_Kp_slave_2000_Ki_slave_4_Kd_slave_1',
        'Kp_master_2000_Ki_master_4_Kd_master_1_Kn_master_400_Kp_slave_2000_Ki_slave_4_Kd_slave_1'

    ]

    pid_controller_captions = [
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 4)} \\quad {add_type_k_latex('d', 1.2)} \\quad {add_type_k_latex('n',400)} \\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',4,is_master=False)} \quad {add_type_k_latex('d',1,is_master=False)}",
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 4)} \\quad {add_type_k_latex('d', 1)}  \\quad {add_type_k_latex('n',200)}\\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',4,is_master=False)} \quad {add_type_k_latex('d',1,is_master=False)}",
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 4)} \\quad {add_type_k_latex('d', 1)} \\quad {add_type_k_latex('n',400)} \\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',4,is_master=False)} \quad {add_type_k_latex('d',1,is_master=False)}"
    ]

    dev_pid_controller_figures_name = [
        'Kp_master_2000_Ki_master_6_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_4_Kd_slave_0_001_Kn_slave_2',  # Kp_master_2000_Ki_master_6_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_4_Kd_slave_0_001_Kn_slave_2
        'Kp_master_2000_Ki_master_6_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_6_Kd_slave_0_01_Kn_slave_700', # Kp_master_2000_Ki_master_6_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_6_Kd_slave_0_01_Kn_slave_700
        'Kp_master_2000_Ki_master_6_Kd_master_2_5_Kn_master_400_Kp_slave_2000_Ki_slave_6_Kd_slave_0_01_Kn_slave_700'  #Kp_master_2000_Ki_master_6_Kd_master_1_2_Kn_master_400_Kp_slave_2000_Ki_slave_6_Kd_slave_0_01_Kn_slave_700
    ]

    dev_pid_controller_captions = [
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 6)} \\quad {add_type_k_latex('d', 1.2)}  \\quad {add_type_k_latex('n',400)}  \\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',4,is_master=False)} \\quad {add_type_k_latex('d',0.001,is_master=False)} \\quad {add_type_k_latex('n',2,is_master=False)}",
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 6)} \\quad {add_type_k_latex('d', 1.2)} \\quad {add_type_k_latex('n',400)}  \\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',6,is_master=False)} \\quad {add_type_k_latex('d',0.01,is_master=False)} \\quad {add_type_k_latex('n',700,is_master=False)}",
        f"{add_type_k_latex('p', 2000)} \\quad {add_type_k_latex('i', 6)} \\quad {add_type_k_latex('d', 2.5)} \\quad {add_type_k_latex('n',400)}  \\quad {add_type_k_latex('p', 2000,is_master=False)} \\quad {add_type_k_latex('i',6,is_master=False)} \\quad {add_type_k_latex('d',0.01,is_master=False)} \\quad {add_type_k_latex('n',700,is_master=False)}"
    ]

    windup_pid_controller_figures_name = [
        'Kp_master_200_Ki_master_1_Kd_master_0_01_Kp_slave_200_Ki_slave_2_Kd_slave_100_Kaw_slave_0_002',
        'Kp_master_200_Ki_master_1_Kd_master_0_05_Kp_slave_200_Ki_slave_1_Kd_slave_1_Kaw_slave_0_001',
        'Kp_master_200_Ki_master_1_Kd_master_0_05_Kp_slave_200_Ki_slave_1_Kd_slave_700_Kaw_slave_0_0001'
    ]

    windup_pid_controller_captions = [
        f"{add_type_k_latex('p', 200)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 0.01)} \\quad {add_type_k_latex('p', 200,is_master=False)} \\quad {add_type_k_latex('i',2,is_master=False)} \\quad {add_type_k_latex('d',100,is_master=False)} \\quad {add_type_k_latex('aw',0.002,is_master=False)}",
        f"{add_type_k_latex('p', 200)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 0.05)} \\quad {add_type_k_latex('p', 200,is_master=False)} \\quad {add_type_k_latex('i',1,is_master=False)} \\quad {add_type_k_latex('d',1,is_master=False)} \\quad {add_type_k_latex('aw',0.001,is_master=False)}",
        f"{add_type_k_latex('p', 200)} \\quad {add_type_k_latex('i', 1)} \\quad {add_type_k_latex('d', 0.05)} \\quad {add_type_k_latex('p', 200,is_master=False)} \\quad {add_type_k_latex('i',1,is_master=False)} \\quad {add_type_k_latex('d',700,is_master=False)} \\quad {add_type_k_latex('aw',0.0001,is_master=False)}"
    ]

    main_tex = build_main_tex(master_controller, master_result_dir, p_controller_figures_name, p_controller_captions, pd_controller_figures_name, pd_controller_captions, pi_controller_figures_name,
                              pi_controller_captions, pid_controller_figures_name, pid_controller_captions, dev_pid_controller_figures_name, dev_pid_controller_captions, windup_pid_controller_figures_name, windup_pid_controller_captions)

    print(main_tex)


if __name__ == '__main__':
    result_dir_path = 'resultados/roteiro_c'

    missing_master_controllers_dir_paths = [
        'mestre_PID',
        'mestre_PID_filtro_derivativo'
    ]

    main_tamplate = load_tamplate('tamplates/main_tamplate.tex')
    load_figure_tamplate = load_tamplate('tamplates/load_figure_tampate.tex')
    master_controller = 'PI'

    main_tamplate_variables = {
        'CURRENT_MASTER': master_controller,
        'MASTER_DIR': 'mestre_PI',
        'DEV_PID_CONTROLLER_EVALUATION': '',
        'WINDUP_PID_CONTROLLER_EVALUATION': '',
        'SLAVE_P_CONTROLLER_FIGURES': '',
        'SLAVE_PD_CONTROLLER_FIGURES': '',
        'SLAVE_PI_CONTROLLER_FIGURES': '',
        'SLAVE_PID_CONTROLLER_FIGURES': '',
        'SLAVE_DEV_PID_CONTROLLER_FIGURES': '',
        'SLAVE_WINDUP_PID_CONTROLLER_FIGURES': ''

    }
    load_figure_tamplate_variables = {
        'MASTER_CONTROLLLER': master_controller,
        'SLAVE_CONTROLLER': 'P',
        'FILE_NAME': 'file_name',
        'MATH_CAPTION': 'K_p=10'
    }

    # print(render_template(main_tamplate_variables, main_tamplate))
    # print(render_template(load_figure_tamplate_variables, load_figure_tamplate))

    # render_master_pi()

    render_master_dev_pid()
    pass
