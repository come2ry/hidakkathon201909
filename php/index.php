<?php
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;

require __DIR__ . '/vendor/autoload.php';

$app = AppFactory::create();

$app->get('[/{params:.*}]', function (Request $request, Response $response, $args) {
    $response->getBody()->write("Not Implemented");
    return $response->withStatus(501);
});

$app->run();

