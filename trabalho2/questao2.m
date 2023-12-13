% Questão 2 do trabalho 2
% Autora: Maria Claudia Campos Martins
% Matricula: 170109968

clc
close all

% Le imagem
onionImage = imread('onion.png');

figure(1)
imshow(onionImage)
title('Original Image');

cform = makecform('srgb2lab');
lab_onionImage = applycform(onionImage,cform);

ab = double(lab_onionImage(:,:,2:3));
nrows = size(ab,1);
ncols = size(ab,2);
ab = reshape(ab, nrows*ncols,2);

nColors = 7;
[cluster_idx, cluster_center] = kmeans(ab,nColors, 'distance','sqEuclidean','Replicates',3);

pixel_labels = reshape(cluster_idx, nrows, ncols);
figure(2)
imshow(pixel_labels,[])
title('Cluster index');

segmented_images = cell(1:7);
rgb_label = repmat(pixel_labels, [1 1 3]);

for k = 1:nColors
    color = onionImage;
    color(rgb_label ~= k) = 0;
    segmented_images{k} = color;
end

figure(3)
imshow(segmented_images{1})
title('Objetos no cluster 1');
imwrite(segmented_images{1}, 'img/questao2-cluster-1.png');
figure(4)
imshow(segmented_images{2})
title('Objetos no cluster 2');
imwrite(segmented_images{2}, 'img/questao2-cluster-2.png');
figure(5)
imshow(segmented_images{3})
title('Objetos no cluster 3');
imwrite(segmented_images{3}, 'img/questao2-cluster-3.png');
figure(6)
imshow(segmented_images{4})
title('Objetos no cluster 4');
imwrite(segmented_images{4}, 'img/questao2-cluster-4.png');
figure(7)
imshow(segmented_images{5})
title('Objetos no cluster 5');
imwrite(segmented_images{5}, 'img/questao2-cluster-5.png');
figure(8)
imshow(segmented_images{6})
title('Objetos no cluster 6');
imwrite(segmented_images{6}, 'img/questao2-cluster-6.png');
figure(9)
imshow(segmented_images{7})
title('Objetos no cluster 7');
imwrite(segmented_images{7}, 'img/questao2-cluster-7.png');