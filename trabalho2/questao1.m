% Questão 1 do trabalho 2
% Autora: Maria Claudia Campos Martins
% Matricula: 170109968

clc
close all

% Le imagem
brainImage = imread('brain.png');

% Converte imagem para escala de cinza
brainImageGray = rgb2gray(brainImage);

% Aplica filtro gaussiano passa-baixas
brainImageGaussianFiltered = imgaussfilt(brainImageGray, 0.75);

% Aplica filtro de mediana
brainImageGaussianFiltered_mean = medfilt2(brainImageGaussianFiltered);

% Salva imagem filtrada para processamento futuro
imwrite(uint8(brainImageGaussianFiltered_mean), 'brainFiltered.png');


% Mostra imagens orginal, filtrada com gaussiano e filtrada com mediana
figure(1)
imshow(brainImage);colormap gray
title('Imagem original', 'fontsize', 3)

figure(2)
imshow(abs(brainImageGaussianFiltered), [0 290]); colormap gray;
title('Filtro gaussiano passa-baixas', 'fontsize', 12);
imwrite(abs(brainImageGaussianFiltered), 'img/questao1-filtro-gaussiano.png');

figure(3)
imshow(abs(brainImageGaussianFiltered_mean), [0 290]), colormap gray
title('Filtro de mediana', 'fontsize', 12)
imwrite(abs(brainImageGaussianFiltered_mean), 'img/questao1-filtro-mediana.png');

% Lê imagem filtrada
brainFiltered = imread('brainFiltered.png');

% Gera o histograma
figure(4)
imhist(brainFiltered);
title('Histograma da imagem filtrada', 'fontsize', 12);

% Aplica binarizacao observando histograma
bw = (brainFiltered > 174 );

% Mostra imagem binarizada
figure(5)
imshow(bw), colormap gray
title('Imagem binarizada', 'fontsize', 12)
imwrite(bw, 'img/questao1-binarizada.png');

% Gera disco para abertura
se = strel('disk',2);

% Faz abertura
afterOpening = imopen(bw, se);

% Mostra resultado da abertura
figure(6)
imshow(afterOpening,[]);
title('Imagem após abertura', 'fontsize', 12)
imwrite(afterOpening, 'img/questao1-abertura.png');

% Conta quantos elementos conectados tem na imagem
cc = bwconncomp(afterOpening);

% Idenfica elemento de maior tamanho e o remove (pois eh a margem
% da imagem)
numPixels = cellfun(@numel, cc.PixelIdxList);
[biggest,idx] = max(numPixels);
afterOpening(cc.PixelIdxList{idx}) = 0;
 
% Mostra a imagem com apenas o tumor
figure(7)
imshow(afterOpening)
title('Imagem apenas com o tumor', 'fontsize', 12)
imwrite(afterOpening, 'img/questao1-tumor.png');
