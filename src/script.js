// Organização dos dados
const db = {
  produtos: JSON.parse(localStorage.getItem('dbProdutos')) || [],
  vendas: JSON.parse(localStorage.getItem('dbVendas')) || [],
  clientes: JSON.parse(localStorage.getItem('dbClientes')) || []
};

// Estado da aplicação
const estado = {
  visualizacaoAtual: 'produtos',
  idProdutoEditando: null,
  idVendaEditando: null,
  idClienteEditando: null
};

// Elementos DOM - Organizados por categoria
const elementos = {
  visualizacoes: {
    produtos: document.getElementById('produtos-view'),
    vendas: document.getElementById('vendas-view'),
    clientes: document.getElementById('clientes-view')
  },
  botoes: {
    produtos: document.getElementById('view-produtos'),
    vendas: document.getElementById('view-vendas'),
    clientes: document.getElementById('view-clientes'),
    incluir: document.getElementById('new')
  },
  modais: {
    produtos: document.querySelector('#modal-produtos'),
    vendas: document.querySelector('#modal-vendas'),
    clientes: document.querySelector('#modal-clientes')
  },
  tabelas: {
    produtos: document.querySelector('#produtos-tbody'),
    vendas: document.querySelector('#vendas-tbody'),
    clientes: document.querySelector('#clientes-tbody')
  },
  formularios: {
    produtos: {
      nome: document.querySelector('#m-produto'),
      descricao: document.querySelector('#m-descriacao'),
      preco: document.querySelector('#m-preco'),
      salvar: document.querySelector('#btnSalvarProduto')
    },
    vendas: {
      produto: document.querySelector('#v-produto'),
      data: document.querySelector('#v-data'),
      quantidade: document.querySelector('#v-quantidade'),
      desconto: document.querySelector('#v-desconto'),
      status: document.querySelector('#v-status'),
      salvar: document.querySelector('#btnSalvarVenda')
    },
    clientes: {
      nome: document.querySelector('#c-nome'),
      email: document.querySelector('#c-email'),
      cpf: document.querySelector('#c-cpf'),
      salvar: document.querySelector('#btnSalvarCliente')
    }
  }
};

// FUNÇÕES DE UTILIDADE 

// Validar CPF
function validarCPF(cpf) {
  cpf = cpf.replace(/[^\d]+/g, '');
  
  if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
  
  // Validação do primeiro dígito verificador
  let soma = 0;
  for (let i = 0; i < 9; i++) {
    soma += parseInt(cpf.charAt(i)) * (10 - i);
  }
  
  let resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.charAt(9))) return false;
  
  // Validação do segundo dígito verificador
  soma = 0;
  for (let i = 0; i < 10; i++) {
    soma += parseInt(cpf.charAt(i)) * (11 - i);
  }
  
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.charAt(10))) return false;
  
  return true;
}

// Validar email
function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// Formatar CPF
function formatarCPF(cpf) {
  cpf = cpf.replace(/\D/g, ''); // Remove não-dígitos
  
  if (cpf.length > 11) {
    cpf = cpf.slice(0, 11);
  }
  
  if (cpf.length > 9) {
    cpf = cpf.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2})$/, '$1.$2.$3-$4');
  } else if (cpf.length > 6) {
    cpf = cpf.replace(/^(\d{3})(\d{3})(\d{1,3})$/, '$1.$2.$3');
  } else if (cpf.length > 3) {
    cpf = cpf.replace(/^(\d{3})(\d{1,3})$/, '$1.$2');
  }
  
  return cpf;
}

// FUNÇÕES DE GERENCIAMENTO DE DADOS

// Salvar no LocalStorage
function salvarDados() {
  localStorage.setItem('dbProdutos', JSON.stringify(db.produtos));
  localStorage.setItem('dbVendas', JSON.stringify(db.vendas));
  localStorage.setItem('dbClientes', JSON.stringify(db.clientes));
}

// FUNÇÕES DE INTERFACE

// Alternar entre as visualizações
function toggleView(vista) {
  alterarVisualizacao(vista);
}

// Alternar entre as visualizações
function alterarVisualizacao(vista) {
  // Esconder todas as visualizações
  elementos.visualizacoes.produtos.style.display = 'none';
  elementos.visualizacoes.vendas.style.display = 'none';
  elementos.visualizacoes.clientes.style.display = 'none';
  
  // Remover classe ativa de todos os botões
  elementos.botoes.produtos.classList.remove('active-view');
  elementos.botoes.vendas.classList.remove('active-view');
  elementos.botoes.clientes.classList.remove('active-view');
  
  // Mostrar apenas a vista selecionada e ativar o botão correspondente
  if (vista === 'produtos') {
    elementos.visualizacoes.produtos.style.display = 'block';
    elementos.botoes.produtos.classList.add('active-view');
  } else if (vista === 'vendas') {
    elementos.visualizacoes.vendas.style.display = 'block';
    elementos.botoes.vendas.classList.add('active-view');
  } else if (vista === 'clientes') {
    elementos.visualizacoes.clientes.style.display = 'block';
    elementos.botoes.clientes.classList.add('active-view');
  }
  
  estado.visualizacaoAtual = vista;
}

// Abrir o modal apropriado
function openModal() {
  abrirModal();
}

function abrirModal(editar = false, id = null) {
  if (estado.visualizacaoAtual === 'produtos') {
    // Resetar ou preencher o formulário
    if (editar && id !== null) {
      elementos.formularios.produtos.nome.value = db.produtos[id].nome;
      elementos.formularios.produtos.descricao.value = db.produtos[id].descricao;
      elementos.formularios.produtos.preco.value = db.produtos[id].preco;
      estado.idProdutoEditando = id;
    } else {
      elementos.formularios.produtos.nome.value = '';
      elementos.formularios.produtos.descricao.value = '';
      elementos.formularios.produtos.preco.value = '';
      estado.idProdutoEditando = null;
    }
    elementos.modais.produtos.classList.add('active');
    
  } else if (estado.visualizacaoAtual === 'vendas') {
    atualizarDropdownProdutos();
    
    if (editar && id !== null) {
      elementos.formularios.vendas.produto.value = db.vendas[id].produtoId;
      elementos.formularios.vendas.data.value = db.vendas[id].data;
      elementos.formularios.vendas.quantidade.value = db.vendas[id].quantidade;
      elementos.formularios.vendas.desconto.value = db.vendas[id].desconto;
      elementos.formularios.vendas.status.value = db.vendas[id].status;
      estado.idVendaEditando = id;
    } else {
      const hoje = new Date().toISOString().split('T')[0];
      elementos.formularios.vendas.data.value = hoje;
      elementos.formularios.vendas.produto.value = '';
      elementos.formularios.vendas.quantidade.value = '1';
      elementos.formularios.vendas.desconto.value = '0';
      elementos.formularios.vendas.status.value = 'Pendente';
      estado.idVendaEditando = null;
    }
    elementos.modais.vendas.classList.add('active');
    
  } else if (estado.visualizacaoAtual === 'clientes') {
    if (editar && id !== null) {
      elementos.formularios.clientes.nome.value = db.clientes[id].nome;
      elementos.formularios.clientes.email.value = db.clientes[id].email;
      elementos.formularios.clientes.cpf.value = db.clientes[id].cpf;
      estado.idClienteEditando = id;
    } else {
      elementos.formularios.clientes.nome.value = '';
      elementos.formularios.clientes.email.value = '';
      elementos.formularios.clientes.cpf.value = '';
      estado.idClienteEditando = null;
    }
    elementos.modais.clientes.classList.add('active');
  }
}

// Atualizar o dropdown de produtos no formulário de vendas
function atualizarDropdownProdutos() {
  const select = elementos.formularios.vendas.produto;
  // Limpar opções atuais
  select.innerHTML = '<option value="">Selecione um produto</option>';
  
  // Adicionar produtos do banco de dados
  db.produtos.forEach((produto, index) => {
    const option = document.createElement('option');
    option.value = index;
    option.textContent = produto.nome;
    select.appendChild(option);
  });
}

// FUNÇÕES DE RENDERIZAÇÃO DAS TABELAS

// Renderizar tabela de produtos
function renderizarTabelaProdutos() {
  elementos.tabelas.produtos.innerHTML = '';
  
  db.produtos.forEach((produto, index) => {
    const tr = document.createElement('tr');
    
    tr.innerHTML = `
      <td>${produto.nome}</td>
      <td>${produto.descricao}</td>
      <td>R$ ${parseFloat(produto.preco).toFixed(2)}</td>
      <td class="acao">
        <button onclick="editarProduto(${index})"><i class='bx bx-edit'></i></button>
      </td>
      <td class="acao">
        <button onclick="excluirProduto(${index})"><i class='bx bx-trash'></i></button>
      </td>
    `;
    
    elementos.tabelas.produtos.appendChild(tr);
  });
}

// Renderizar tabela de vendas
function renderizarTabelaVendas() {
  elementos.tabelas.vendas.innerHTML = '';
  
  db.vendas.forEach((venda, index) => {
    const tr = document.createElement('tr');
    
    // Encontrar o nome do produto pelo ID
    const produtoNome = venda.produtoId !== '' ? 
      db.produtos[parseInt(venda.produtoId)]?.nome || 'Produto não encontrado' : 
      'Produto não encontrado';
    
    // Formatar a data
    const data = new Date(venda.data);
    const dataFormatada = data.toLocaleDateString('pt-BR');
    
    tr.innerHTML = `
      <td>${produtoNome}</td>
      <td>${dataFormatada}</td>
      <td>${venda.quantidade}</td>
      <td>${venda.desconto}%</td>
      <td>
        <span class="status-${venda.status.toLowerCase()}">${venda.status}</span>
      </td>
      <td class="acao">
        <button onclick="editarVenda(${index})"><i class='bx bx-edit'></i></button>
      </td>
      <td class="acao">
        <button onclick="excluirVenda(${index})"><i class='bx bx-trash'></i></button>
      </td>
    `;
    
    elementos.tabelas.vendas.appendChild(tr);
  });
}

// Renderizar tabela de clientes
function renderizarTabelaClientes() {
  elementos.tabelas.clientes.innerHTML = '';
  
  db.clientes.forEach((cliente, index) => {
    const tr = document.createElement('tr');
    
    tr.innerHTML = `
      <td>${cliente.nome}</td>
      <td>${cliente.email}</td>
      <td>${cliente.cpf}</td>
      <td class="acao">
        <button onclick="editarCliente(${index})"><i class='bx bx-edit'></i></button>
      </td>
      <td class="acao">
        <button onclick="excluirCliente(${index})"><i class='bx bx-trash'></i></button>
      </td>
    `;
    
    elementos.tabelas.clientes.appendChild(tr);
  });
}

// FUNÇÕES DE AÇÃO (CRUD)

// Editar produto
function editarProduto(id) {
  abrirModal(true, id);
}

// Excluir produto
function excluirProduto(id) {
  // Verificar se o produto está sendo usado em alguma venda
  const produtoUsado = db.vendas.some(venda => parseInt(venda.produtoId) === id);
  
  if (produtoUsado) {
    alert('Este produto não pode ser excluído pois está associado a vendas.');
    return;
  }
  
  if (confirm('Deseja realmente excluir este produto?')) {
    db.produtos.splice(id, 1);
    
    // Atualizar IDs das vendas que referenciam produtos com índices mais altos
    db.vendas.forEach(venda => {
      if (parseInt(venda.produtoId) > id) {
        venda.produtoId = String(parseInt(venda.produtoId) - 1);
      }
    });
    
    salvarDados();
    renderizarTabelaProdutos();
    renderizarTabelaVendas();
  }
}

// Editar venda
function editarVenda(id) {
  abrirModal(true, id);
}

// Excluir venda
function excluirVenda(id) {
  if (confirm('Deseja realmente excluir esta venda?')) {
    db.vendas.splice(id, 1);
    salvarDados();
    renderizarTabelaVendas();
  }
}

// Editar cliente
function editarCliente(id) {
  abrirModal(true, id);
}

// Excluir cliente
function excluirCliente(id) {
  if (confirm('Deseja realmente excluir este cliente?')) {
    db.clientes.splice(id, 1);
    salvarDados();
    renderizarTabelaClientes();
  }
}

// EVENTOS

// Evento para formatar CPF enquanto digita
elementos.formularios.clientes.cpf.addEventListener('input', function(e) {
  e.target.value = formatarCPF(e.target.value);
});

// Eventos para fechar modais quando clicar fora
elementos.modais.produtos.addEventListener('click', e => {
  if (e.target.className.indexOf('modal-container') !== -1) {
    elementos.modais.produtos.classList.remove('active');
  }
});

elementos.modais.vendas.addEventListener('click', e => {
  if (e.target.className.indexOf('modal-container') !== -1) {
    elementos.modais.vendas.classList.remove('active');
  }
});

elementos.modais.clientes.addEventListener('click', e => {
  if (e.target.className.indexOf('modal-container') !== -1) {
    elementos.modais.clientes.classList.remove('active');
  }
});

// Eventos para os botões de salvar

// Salvar produto
elementos.formularios.produtos.salvar.addEventListener('click', e => {
  e.preventDefault();
  
  const nome = elementos.formularios.produtos.nome.value;
  const descricao = elementos.formularios.produtos.descricao.value;
  const preco = elementos.formularios.produtos.preco.value;
  
  if (nome === '' || descricao === '' || preco === '') {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  if (estado.idProdutoEditando !== null) {
    // Atualizar produto existente
    db.produtos[estado.idProdutoEditando] = { nome, descricao, preco };
  } else {
    // Adicionar novo produto
    db.produtos.push({ nome, descricao, preco });
  }

  salvarDados();
  elementos.modais.produtos.classList.remove('active');
  renderizarTabelaProdutos();
});

// Salvar venda
elementos.formularios.vendas.salvar.addEventListener('click', e => {
  e.preventDefault();
  
  const produtoId = elementos.formularios.vendas.produto.value;
  const data = elementos.formularios.vendas.data.value;
  const quantidade = elementos.formularios.vendas.quantidade.value;
  const desconto = elementos.formularios.vendas.desconto.value;
  const status = elementos.formularios.vendas.status.value;
  
  if (produtoId === '' || data === '' || quantidade === '' || desconto === '' || status === '') {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  if (estado.idVendaEditando !== null) {
    // Atualizar venda existente
    db.vendas[estado.idVendaEditando] = { produtoId, data, quantidade, desconto, status };
  } else {
    // Adicionar nova venda
    db.vendas.push({ produtoId, data, quantidade, desconto, status });
  }

  salvarDados();
  elementos.modais.vendas.classList.remove('active');
  renderizarTabelaVendas();
});

// Salvar cliente
elementos.formularios.clientes.salvar.addEventListener('click', e => {
  e.preventDefault();
  
  const nome = elementos.formularios.clientes.nome.value;
  const email = elementos.formularios.clientes.email.value;
  const cpf = elementos.formularios.clientes.cpf.value;
  
  if (nome === '' || email === '' || cpf === '') {
    alert('Por favor, preencha todos os campos.');
    return;
  }
  
  // Validação de email
  if (!validarEmail(email)) {
    alert('Por favor, insira um email válido.');
    return;
  }
  
  // Validação de CPF
  const cpfLimpo = cpf.replace(/[^\d]+/g, '');
  if (!validarCPF(cpfLimpo)) {
    alert('Por favor, insira um CPF válido.');
    return;
  }
  
  // Verificar se o CPF já existe (apenas para novos clientes)
  if (estado.idClienteEditando === null) {
    const cpfExistente = db.clientes.some(cliente => 
      cliente.cpf.replace(/[^\d]+/g, '') === cpfLimpo
    );
    
    if (cpfExistente) {
      alert('Este CPF já está cadastrado no sistema.');
      return;
    }
  }

  if (estado.idClienteEditando !== null) {
    // Atualizar cliente existente
    db.clientes[estado.idClienteEditando] = { nome, email, cpf };
  } else {
    // Adicionar novo cliente
    db.clientes.push({ nome, email, cpf });
  }

  salvarDados();
  elementos.modais.clientes.classList.remove('active');
  renderizarTabelaClientes();
});

// INICIALIZAÇÃO

// Configurar botões de navegação
elementos.botoes.produtos.addEventListener('click', () => alterarVisualizacao('produtos'));
elementos.botoes.vendas.addEventListener('click', () => alterarVisualizacao('vendas'));
elementos.botoes.clientes.addEventListener('click', () => alterarVisualizacao('clientes'));

// Configurar botão Incluir
if (elementos.botoes.incluir) {
  elementos.botoes.incluir.addEventListener('click', () => abrirModal());
}

// Disponibilizar funções globalmente para as chamadas diretas do HTML
window.openModal = openModal;
window.toggleView = toggleView;
window.editarProduto = editarProduto;
window.excluirProduto = excluirProduto;
window.editarVenda = editarVenda;
window.excluirVenda = excluirVenda;
window.editarCliente = editarCliente;
window.excluirCliente = excluirCliente;

// Carregar dados iniciais
renderizarTabelaProdutos();
renderizarTabelaVendas();
renderizarTabelaClientes();

// Iniciar com visualização de produtos
alterarVisualizacao('produtos');