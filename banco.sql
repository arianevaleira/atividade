CREATE TABLE IF NOT  EXISTS tb_usuarios (
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_senha TEXT NOT NULL,
    usu_email TEXT NOT NULL,
    usu_mat TEXT NOT NULL
);

CREATE TABLE IF NOT  EXISTS tb_exercicios (
    exe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exe_nome TEXT NOT NULL,
    exe_descricao TEXT NOT NULL,
    exe_usu_mat INT NOT NULL,
    FOREIGN KEY (exe_usu_mat) REFERENCES tb_usuarios(usu_mat)
);