import json


def load_template(template_path: str) -> str:
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except OSError:
        print(f'Unable to load template: {template_path}')
        exit(1)


def render_template(variables: dict, tamplate: str) -> str:
    renderized_tamplate = tamplate
    for key in variables:
        renderized_tamplate = renderized_tamplate.replace(
            f'%{key}%', variables[key])

    return renderized_tamplate


def load_controller_data_from_json(json_file_name: str) -> dict:
    try:
        with open(json_file_name, 'r') as json_file:
            pi_controller_data = json.load(json_file)

    except OSError:
        print(
            f'arquivo {json_file_name} não encontrado !! está executando o script dentro do diretorio render_tex ?')
        exit(1)

    return pi_controller_data


def build_controller_figures_tex(master_controller: str, slave_controller: str, figure_names: list, captions: list) -> str:

    slave_names = {
        'p':'P',
        'pd':'PD',
        'pi':'PI',
        'pid':'PID',
        'dev_pid':'PID filtro derivativo',
        'windup_pid':'PID filtro windup'
    }

    load_figure_tamplate_variables = {
        'MASTER_CONTROLLER': master_controller,
        'SLAVE_CONTROLLER': slave_names[slave_controller],
        'FILE_NAME': 'None',
        'MATH_CAPTION': 'None'
    }

    renderized_templates = list()
    load_figure_template = load_template('tamplates/load_figure_tampate.tex')

    for figure_name, caption in zip(figure_names, captions):
        load_figure_tamplate_variables['FILE_NAME'] = figure_name
        load_figure_tamplate_variables['MATH_CAPTION'] = caption

        renderized_templates += render_template(
            load_figure_tamplate_variables, load_figure_template) + '\n'

    return ''.join(renderized_templates)


def build_all_controller_types_figures(controller_data: dict) -> dict:
    controller_figures = dict()
    for controller_type in ['p', 'pd', 'pi', 'pid', 'dev_pid', 'windup_pid']:
        controller_figures[controller_type] = build_controller_figures_tex(controller_data['master_controller'], controller_type,
                                                                           controller_data[f'{controller_type}_controller_figures_name'], controller_data[f'{controller_type}_controller_captions'])
    return controller_figures


def build_main_tex(controller_data: dict):

    controller_figures = build_all_controller_types_figures(controller_data)

    main_tamplate_variables = {
        'CURRENT_MASTER': controller_data['master_controller'],
        'MASTER_DIR': controller_data['master_dir'],
        'SLAVE_P_CONTROLLER_FIGURES': controller_figures['p'],
        'SLAVE_PD_CONTROLLER_FIGURES': controller_figures['pd'],
        'SLAVE_PI_CONTROLLER_FIGURES': controller_figures['pi'],
        'SLAVE_PID_CONTROLLER_FIGURES': controller_figures['pid'],
        'SLAVE_DEV_PID_CONTROLLER_FIGURES': controller_figures['dev_pid'],
        'SLAVE_WINDUP_PID_CONTROLLER_FIGURES': controller_figures['windup_pid']
    }
    main_template = load_template('tamplates/main_tamplate.tex')
    main_tex = render_template(main_tamplate_variables, main_template)
    return main_tex


def build_controller_tex_from_json(json_file_name: str):

    pi_controller_data = load_controller_data_from_json(json_file_name)

    main_tex = build_main_tex(pi_controller_data)

    print(main_tex)


if __name__ == '__main__':
    # build_controller_tex_from_json('pi_controller.json')
    build_controller_tex_from_json('pid_controller.json')
    # build_controller_tex_from_json('dev_pid_controller.json')

    pass
